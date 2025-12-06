# chatbot_service.py
from backend.services.llm_service import LLMService
from backend.services.rag_service import RAGService
from backend.models import User, ChatMessage, Doctor, AvailabilitySlot, Appointment, Patient, Billing, Department, EscalationTicket
from backend.extensions import db
from datetime import datetime, timedelta, date
import re
import json
from typing import Dict, List, Optional, Tuple
from sqlalchemy import and_, or_

class ChatbotService:
    """
    Premium FalcoVita AI - Hospital Management Assistant
    Complete implementation with role-based behavior, medical safety, and workflow automation
    """

    # Role-based permission matrix
    ROLE_PERMISSIONS = {
        'admin': {
            'can_view_all': True,
            'can_manage_appointments': True,
            'can_view_billing': True,
            'can_view_reports': True,
            'can_manage_doctors': True,
            'can_view_patients': True,
            'can_escalate': True,
            'can_cancel_any': True,
            'can_book_for_others': True
        },
        'doctor': {
            'can_view_all': False,
            'can_manage_appointments': False,
            'can_view_billing': False,
            'can_view_reports': False,
            'can_manage_doctors': False,
            'can_view_patients': True,  # Only assigned
            'can_escalate': True,
            'can_cancel_any': False,
            'can_book_for_others': False,
            'can_view_own_schedule': True,
            'can_view_assigned_patients': True
        },
        'receptionist': {
            'can_view_all': False,
            'can_manage_appointments': True,
            'can_view_billing': False,
            'can_view_reports': False,
            'can_manage_doctors': False,
            'can_view_patients': True,
            'can_escalate': True,
            'can_cancel_any': True,
            'can_book_for_others': True
        },
        'nurse': {
            'can_view_all': False,
            'can_manage_appointments': False,
            'can_view_billing': False,
            'can_view_reports': False,
            'can_manage_doctors': False,
            'can_view_patients': True,  # Only assigned
            'can_escalate': True,
            'can_cancel_any': False,
            'can_book_for_others': False,
            'can_view_vitals': True,
            'can_view_assigned_patients': True
        },
        'patient': {
            'can_view_all': False,
            'can_manage_appointments': True,  # Only own
            'can_view_billing': True,  # Only own
            'can_view_reports': False,
            'can_manage_doctors': False,
            'can_view_patients': False,
            'can_escalate': True,
            'can_cancel_any': False,
            'can_book_for_others': False,
            'can_view_own_data': True
        }
    }

    @staticmethod
    def get_chat_history(user_id, limit=10):
        messages = ChatMessage.query.filter_by(user_id=user_id).order_by(ChatMessage.created_at.desc()).limit(limit).all()
        return messages[::-1]

    @staticmethod
    def save_message(user_id, role, content, action_data=None):
        msg = ChatMessage(
            user_id=user_id,
            role=role,
            content=content,
            action_data=json.dumps(action_data) if action_data else None
        )
        db.session.add(msg)
        db.session.commit()
        return msg

    @staticmethod
    def _resolve_role(user_id):
        user = User.query.get(user_id)
        if not user:
            return None, {"error": "User not found"}
        return user, user.role.lower()

    @staticmethod
    def _check_permission(role: str, permission: str) -> bool:
        """Check if role has specific permission"""
        return ChatbotService.ROLE_PERMISSIONS.get(role, {}).get(permission, False)

    @staticmethod
    def process_message(user_id, message):
        """
        Premium message processing with FalcoVita AI capabilities
        """
        user, role_or_err = ChatbotService._resolve_role(user_id)
        if user is None:
            return role_or_err

        role = role_or_err

        # Save user message
        ChatbotService.save_message(user_id, 'user', message)

        # Retrieve history for context
        history = ChatbotService.get_chat_history(user_id, limit=15)
        history_text = "\n".join([f"{m.role.upper()}: {m.content}" for m in history])

        # Get user profile for context
        user_info = f"User: {user.name}, Role: {role.upper()}, ID: {user_id}"

        # RAG retrieval with enhanced context
        context = RAGService.retrieve_context(
            message, 
            role, 
            user_id,
            additional_context={"user_info": user_info, "history": history_text[:500]}
        )

        # Generate response via LLM with premium prompt
        llm_output = LLMService.generate_premium_response(
            message=message,
            user_role=role,
            user_id=user_id,
            context=context,
            history=history_text,
            user_info=user_info
        )
        
        # Handle LLM output
        if isinstance(llm_output, str):
            llm_output = {"text": llm_output, "action": None}

        text_response = llm_output.get('text', '')
        action_data = llm_output.get('action')

        # Server-side action enrichment with real data
        enriched_action = ChatbotService._enrich_action(action_data, message, role, user_id)

        # Save assistant response
        ChatbotService.save_message(user_id, 'assistant', text_response, enriched_action)

        return {
            "text": text_response, 
            "action": enriched_action, 
            "role": role,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat()
        }

    @staticmethod
    def _enrich_action(action, message, role, user_id):
        """
        Enrich actions with real database data for reliability
        """
        if not action:
            return None

        act = action.copy()
        action_type = act.get('action')
        data = act.get('data', {})

        # CHECK AVAILABILITY / BOOK APPOINTMENT
        if action_type in ('check_availability', 'book_appointment', 'suggest_slots'):
            # Extract doctor info
            doctor_query = data.get('doctor_name') or data.get('doctor_id') or \
                          ChatbotService._extract_doctor_name_from_text(message) or \
                          ChatbotService._extract_department_from_text(message)
            
            date_str = data.get('date') or ChatbotService._extract_date_from_text(message)
            preferred_time = data.get('preferred_time') or ChatbotService._extract_preferred_time(message)

            # Find doctor
            doctor = None
            if doctor_query:
                if isinstance(doctor_query, int) or doctor_query.isdigit():
                    doctor = Doctor.query.get(int(doctor_query))
                else:
                    # Search by name or department
                    if 'department' in doctor_query.lower() or any(dept in doctor_query.lower() for dept in ['cardiology', 'orthopedic', 'pediatric']):
                        dept_name = ChatbotService._extract_department_from_text(doctor_query)
                        if dept_name:
                            doctors = Doctor.query.join(User).join(Department).filter(
                                Department.name.ilike(f"%{dept_name}%")
                            ).limit(5).all()
                            if doctors:
                                doctor = doctors[0]
                                data['department'] = dept_name
                    else:
                        doctors = Doctor.query.join(User).filter(
                            User.name.ilike(f"%{doctor_query}%")
                        ).limit(5).all()
                        if doctors:
                            doctor = doctors[0]

            if doctor:
                data['doctor_id'] = doctor.id
                data['doctor_name'] = doctor.user.name
                data.pop('doctor_name', None)
                
                # Get available slots
                slots = ChatbotService._get_available_slots_for_doc(doctor.id, date_str)
                if slots:
                    data['slots'] = slots[:8]  # Limit to 8 slots for UX
                    
                    # If preferred time, prioritize matching slots
                    if preferred_time:
                        matching_slots = [s for s in slots if preferred_time in s]
                        if matching_slots:
                            data['preferred_slots'] = matching_slots

            # FALLBACK: If checking availability but no doctor found, suggest doctors
            elif action_type == 'check_availability':
                doctors = Doctor.query.join(User).limit(4).all()
                act['action'] = 'choices'
                act['data']['options'] = [f"Check {d.user.name}" for d in doctors if d.user]
                return act

            # Normalize date
            if date_str:
                try:
                    parsed = ChatbotService._parse_natural_date(date_str)
                    data['date'] = parsed.strftime("%Y-%m-%d")
                    data['day_name'] = parsed.strftime("%A")
                except:
                    pass

            if preferred_time:
                data['preferred_time'] = preferred_time

            act['data'] = data
            return act

        # CANCEL APPOINTMENT
        if action_type == 'cancel_appointment':
            appt_id = data.get('appointment_id')
            if not appt_id:
                # Try to find appointment from context
                appt = ChatbotService._find_appointment_from_context(message, user_id, role)
                if appt:
                    data['appointment_id'] = appt.id
                    data['doctor_name'] = appt.doctor.user.name
                    data['date'] = appt.date.strftime("%Y-%m-%d") if appt.date else None
                    data['time'] = appt.time
                    
            act['data'] = data
            return act

        # SEARCH DOCTORS
        if action_type == 'search_doctors':
            department = data.get('department') or ChatbotService._extract_department_from_text(message)
            if department:
                data['department'] = department
                # Get doctors in department
                doctors = ChatbotService._get_doctors_by_department(department)
                if doctors:
                    data['doctors'] = doctors[:5]  # Limit to 5
            
            name_query = data.get('name') or ChatbotService._extract_doctor_name_from_text(message)
            if name_query:
                data['name'] = name_query
            
            act['data'] = data
            return act

        # VIEW APPOINTMENTS
        if action_type == 'view_appointments':
            # Determine whose appointments to view
            if role == 'patient':
                data['patient_id'] = user_id
            elif role == 'doctor':
                data['doctor_id'] = user_id
            elif 'patient_name' in data or 'patient_id' in data:
                # Check permission to view other's appointments
                if not ChatbotService._check_permission(role, 'can_book_for_others'):
                    data['patient_id'] = user_id  # Default to own
            
            date_filter = data.get('date') or ChatbotService._extract_date_from_text(message)
            if date_filter:
                data['date'] = date_filter
            
            act['data'] = data
            return act

        # GET BILLING INFO
        if action_type == 'get_billing_info':
            # For patients, only show their own billing
            if role == 'patient':
                data['patient_id'] = user_id
            # For others, check permission
            elif 'patient_id' not in data and not ChatbotService._check_permission(role, 'can_view_billing'):
                return None  # No permission
            
            act['data'] = data
            return act

        # ESCALATE TO HUMAN
        if action_type == 'escalate_to_human':
            data['requested_by'] = user_id
            data['user_role'] = role
            data['timestamp'] = datetime.utcnow().isoformat()
            
            # Extract reason from message
            if 'reason' not in data:
                data['reason'] = message[:200]  # Truncate
            
            act['data'] = data
            return act

        # CHOICES (Suggestions)
        if action_type == 'choices':
            # Role-based suggestions
            base_options = ["Check availability", "Book appointment", "Cancel appointment"]
            
            if role == 'admin':
                options = base_options + ["View reports", "Manage doctors", "Billing overview"]
            elif role == 'doctor':
                options = ["View my schedule", "View my patients", "Check availability"] + base_options
            elif role == 'patient':
                options = base_options + ["View my appointments", "View billing", "Find a doctor"]
            elif role in ['receptionist', 'staff']:
                options = base_options + ["Register patient", "View all appointments", "Check doctor schedules"]
            elif role == 'nurse':
                options = ["View assigned patients", "View schedules", "Check vitals"] + base_options
            else:
                options = base_options
            
            # Filter to unique options
            data['options'] = list(dict.fromkeys(options))[:6]  # Max 6 options
            
            act['data'] = data
            return act

        # DEFAULT: return enriched action
        return act

    @staticmethod
    def _get_available_slots_for_doc(doctor_id, date_iso=None):
        """
        Get available slots for a doctor with intelligent time handling
        """
        slots = []
        today = datetime.utcnow().date()
        
        query = AvailabilitySlot.query.filter_by(
            doctor_id=doctor_id, 
            status='available'
        )
        
        if date_iso:
            try:
                query = query.filter(AvailabilitySlot.date == date_iso)
            except:
                pass
        else:
            # Default: next 7 days
            next_week = today + timedelta(days=7)
            query = query.filter(AvailabilitySlot.date.between(today, next_week))
        
        avail_slots = query.order_by(AvailabilitySlot.date, AvailabilitySlot.time_slot).limit(30).all()
        
        for slot in avail_slots:
            slot_date = slot.date if slot.date else today
            slot_time = slot.time_slot
            
            # Format for display
            if '-' in slot_time:
                try:
                    start_str, end_str = slot_time.split('-')
                    start_time = datetime.strptime(start_str.strip(), "%H:%M").time()
                    end_time = datetime.strptime(end_str.strip(), "%H:%M").time()
                    
                    # Generate hourly slots within range
                    current = datetime.combine(slot_date, start_time)
                    end_dt = datetime.combine(slot_date, end_time)
                    
                    while current < end_dt:
                        slots.append({
                            "time": current.strftime("%H:%M"),
                            "date": slot_date.strftime("%Y-%m-%d"),
                            "day": slot_date.strftime("%A"),
                            "full_display": f"{slot_date.strftime('%A, %b %d')} at {current.strftime('%I:%M %p')}"
                        })
                        current += timedelta(hours=1)
                except:
                    slots.append({
                        "time": slot_time,
                        "date": slot_date.strftime("%Y-%m-%d"),
                        "full_display": f"{slot_date.strftime('%A, %b %d')} at {slot_time}"
                    })
            else:
                slots.append({
                    "time": slot_time,
                    "date": slot_date.strftime("%Y-%m-%d"),
                    "full_display": f"{slot_date.strftime('%A, %b %d')} at {slot_time}"
                })
        
        return slots[:20]  # Limit to 20 slots

    @staticmethod
    def _extract_doctor_name_from_text(text):
        """Enhanced doctor name extraction"""
        patterns = [
            r"(?:dr\.?|doctor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,2})",
            r"with\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"appointment\s+with\s+([A-Z].+?)(?:\s+on|\s+for|$)",
            r"see\s+([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"book\s+with\s+([A-Z].+?)(?:\s+on|\s+for|$)"
        ]
        
        text_lower = text.lower()
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Remove titles
                name = re.sub(r'^(dr\.?|doctor|professor|prof\.?)\s+', '', name, flags=re.IGNORECASE)
                return name
        
        # Check for known doctor names in database
        words = re.findall(r'\b[A-Z][a-z]+\b', text)
        for word in words:
            if len(word) > 2:  # Avoid short words
                doctors = Doctor.query.join(User).filter(User.name.ilike(f"%{word}%")).first()
                if doctors:
                    return doctors.user.name.split()[0]  # Return first name
        
        return None

    @staticmethod
    def _extract_date_from_text(text):
        """Enhanced date extraction with natural language"""
        text_lower = text.lower()
        
        # Today
        if any(word in text_lower for word in ['today', 'now', 'right now']):
            return datetime.utcnow().strftime("%Y-%m-%d")
        
        # Tomorrow
        if 'tomorrow' in text_lower:
            return (datetime.utcnow() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        # Day after tomorrow
        if 'day after tomorrow' in text_lower:
            return (datetime.utcnow() + timedelta(days=2)).strftime("%Y-%m-%d")
        
        # Next week
        if 'next week' in text_lower:
            return (datetime.utcnow() + timedelta(days=7)).strftime("%Y-%m-%d")
        
        # Weekdays
        weekdays = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }
        
        for day, offset in weekdays.items():
            if day in text_lower:
                today = datetime.utcnow()
                days_ahead = (offset - today.weekday() + 7) % 7
                if days_ahead == 0:  # Today is that day
                    days_ahead = 7
                return (today + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        
        # Specific dates (YYYY-MM-DD, MM/DD/YYYY, etc.)
        iso_match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', text)
        if iso_match:
            return iso_match.group(1)
        
        us_match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', text)
        if us_match:
            month, day, year = us_match.groups()
            return f"{year}-{month.zfill(2)}-{day.zfill(2)}"
        
        # Relative dates (in X days)
        rel_match = re.search(r'in\s+(\d+)\s+days?', text_lower)
        if rel_match:
            days = int(rel_match.group(1))
            return (datetime.utcnow() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        return None

    @staticmethod
    def _extract_preferred_time(text):
        """Extract preferred time from text"""
        text_lower = text.lower()
        
        # Morning
        if any(word in text_lower for word in ['morning', 'am', '9am', '10am', '11am']):
            return "morning"
        
        # Afternoon
        if any(word in text_lower for word in ['afternoon', '12pm', '1pm', '2pm', '3pm', '4pm']):
            return "afternoon"
        
        # Evening
        if any(word in text_lower for word in ['evening', 'pm', '5pm', '6pm', '7pm', '8pm']):
            return "evening"
        
        # Specific times
        time_match = re.search(r'\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b', text_lower)
        if time_match:
            hour = int(time_match.group(1))
            minute = time_match.group(2) or "00"
            period = time_match.group(3) or ""
            
            if period == 'pm' and hour < 12:
                hour += 12
            elif period == 'am' and hour == 12:
                hour = 0
            
            return f"{hour:02d}:{minute}"
        
        return None

    @staticmethod
    def _extract_department_from_text(text):
        """Extract department name from text"""
        departments = {
            'cardiology': ['heart', 'cardio', 'cardiologist'],
            'orthopedics': ['bone', 'ortho', 'orthopedic', 'orthopaedic'],
            'pediatrics': ['child', 'pediatric', 'kids', 'children'],
            'neurology': ['brain', 'neuro', 'neurologist'],
            'dermatology': ['skin', 'derm', 'dermatologist'],
            'gastroenterology': ['stomach', 'gi', 'gastro'],
            'oncology': ['cancer', 'onco', 'oncologist'],
            'psychiatry': ['mental', 'psych', 'psychiatrist'],
            'radiology': ['xray', 'scan', 'radiologist'],
            'surgery': ['surgical', 'surgeon', 'operation']
        }
        
        text_lower = text.lower()
        
        for dept, keywords in departments.items():
            if any(keyword in text_lower for keyword in [dept] + keywords):
                return dept
        
        return None

    @staticmethod
    def _parse_natural_date(text):
        """Parse natural language date"""
        date_str = ChatbotService._extract_date_from_text(text)
        if date_str:
            return datetime.strptime(date_str, "%Y-%m-%d")
        return datetime.utcnow()

    @staticmethod
    def _find_appointment_from_context(text, user_id, role):
        """Find appointment from message context"""
        # Try to extract appointment ID
        id_match = re.search(r'(?:appointment|apt)\s*#?\s*(\d+)', text, re.IGNORECASE)
        if id_match:
            appt = Appointment.query.get(int(id_match.group(1)))
            if appt and ChatbotService._check_appointment_access(appt, user_id, role):
                return appt
        
        # Try to find by doctor and date
        doctor_name = ChatbotService._extract_doctor_name_from_text(text)
        date_str = ChatbotService._extract_date_from_text(text)
        
        if doctor_name or date_str:
            query = Appointment.query
            
            if role == 'patient':
                query = query.filter_by(patient_id=user_id)
            elif role == 'doctor':
                query = query.filter_by(doctor_id=user_id)
            
            if doctor_name:
                query = query.join(Doctor).join(User).filter(User.name.ilike(f"%{doctor_name}%"))
            
            if date_str:
                query = query.filter_by(date=date_str)
            
            appt = query.order_by(Appointment.created_at.desc()).first()
            if appt and ChatbotService._check_appointment_access(appt, user_id, role):
                return appt
        
        return None

    @staticmethod
    def _check_appointment_access(appointment, user_id, role):
        """Check if user can access this appointment"""
        if role == 'admin' or ChatbotService._check_permission(role, 'can_view_all'):
            return True
        
        if role == 'patient' and appointment.patient_id == user_id:
            return True
        
        if role == 'doctor' and appointment.doctor_id == user_id:
            return True
        
        if role in ['receptionist', 'staff'] and ChatbotService._check_permission(role, 'can_manage_appointments'):
            return True
        
        return False

    @staticmethod
    def _get_doctors_by_department(department_name):
        """Get doctors by department"""
        doctors = Doctor.query.join(User).join(Department).filter(
            Department.name.ilike(f"%{department_name}%")
        ).limit(10).all()
        
        return [
            {
                "id": doc.id,
                "name": doc.user.name,
                "specialization": doc.specialization,
                "department": department_name,
                "availability": "Available" if doc.availability_slots else "Limited"
            }
            for doc in doctors
        ]

    @staticmethod
    def execute_action(user_id, action, data):
        """
        Execute actions with comprehensive permission checks
        Returns result dict or raises Exception
        """
        user = User.query.get(user_id)
        if not user:
            raise Exception("User not found")
        
        role = user.role.lower()
        
        # BOOK APPOINTMENT
        if action == 'book_appointment':
            # Permission check
            if not ChatbotService._check_permission(role, 'can_manage_appointments'):
                raise Exception(f"Role '{role}' cannot book appointments")
            
            # Extract data
            doctor_id = data.get('doctor_id')
            patient_id = data.get('patient_id')
            date_str = data.get('date')
            slot = data.get('slot') or data.get('time')
            
            # Default patient ID for patients
            if not patient_id and role == 'patient':
                patient_id = user_id
            
            # Validation
            if not all([doctor_id, patient_id, date_str, slot]):
                missing = []
                if not doctor_id: missing.append("doctor")
                if not patient_id: missing.append("patient")
                if not date_str: missing.append("date")
                if not slot: missing.append("time slot")
                raise Exception(f"Missing required fields: {', '.join(missing)}")
            
            # Check doctor exists
            doctor = Doctor.query.get(doctor_id)
            if not doctor:
                raise Exception("Doctor not found")
            
            # Check patient exists (if not current user)
            if patient_id != user_id:
                patient = Patient.query.get(patient_id)
                if not patient:
                    raise Exception("Patient not found")
            
            # Check slot availability
            avail_slot = AvailabilitySlot.query.filter_by(
                doctor_id=doctor_id,
                date=date_str,
                status='available'
            ).filter(AvailabilitySlot.time_slot.contains(slot)).first()
            
            if not avail_slot:
                raise Exception(f"Slot {slot} on {date_str} is not available")
            
            # Create appointment
            appointment = Appointment(
                doctor_id=doctor_id,
                patient_id=patient_id,
                date=datetime.strptime(date_str, "%Y-%m-%d").date(),
                time=slot,
                status='confirmed',
                created_by=user_id,
                created_at=datetime.utcnow()
            )
            
            # Mark slot as booked
            avail_slot.status = 'booked'
            
            db.session.add(appointment)
            db.session.commit()
            
            return {
                "appointment_id": appointment.id,
                "doctor_name": doctor.user.name,
                "patient_name": user.name if patient_id == user_id else patient.user.name,
                "date": date_str,
                "time": slot,
                "status": "confirmed",
                "confirmation_number": f"APT-{appointment.id:06d}"
            }
        
        # CHECK AVAILABILITY
        elif action == 'check_availability':
            doctor_id = data.get('doctor_id')
            date_str = data.get('date')
            
            if not doctor_id:
                raise Exception("Doctor ID is required")
            
            slots = ChatbotService._get_available_slots_for_doc(doctor_id, date_str)
            
            doctor = Doctor.query.get(doctor_id)
            doctor_name = doctor.user.name if doctor else "Unknown Doctor"
            
            return {
                "doctor_id": doctor_id,
                "doctor_name": doctor_name,
                "date": date_str or "Next 7 days",
                "available_slots": slots,
                "total_slots": len(slots)
            }
        
        # CANCEL APPOINTMENT
        elif action == 'cancel_appointment':
            appointment_id = data.get('appointment_id')
            
            if not appointment_id:
                raise Exception("Appointment ID is required")
            
            appointment = Appointment.query.get(appointment_id)
            if not appointment:
                raise Exception("Appointment not found")
            
            # Permission check
            if not ChatbotService._check_appointment_access(appointment, user_id, role):
                raise Exception("Not authorized to cancel this appointment")
            
            # Check if appointment is in the future
            appointment_datetime = datetime.combine(appointment.date, datetime.strptime(appointment.time, "%H:%M").time())
            if appointment_datetime < datetime.utcnow():
                raise Exception("Cannot cancel past appointments")
            
            # Update status
            appointment.status = 'cancelled'
            appointment.cancelled_at = datetime.utcnow()
            appointment.cancelled_by = user_id
            
            # Free up the slot
            avail_slot = AvailabilitySlot.query.filter_by(
                doctor_id=appointment.doctor_id,
                date=appointment.date.strftime("%Y-%m-%d"),
                status='booked'
            ).filter(AvailabilitySlot.time_slot.contains(appointment.time)).first()
            
            if avail_slot:
                avail_slot.status = 'available'
            
            db.session.commit()
            
            return {
                "appointment_id": appointment_id,
                "status": "cancelled",
                "cancelled_at": datetime.utcnow().isoformat(),
                "refund_eligible": (datetime.utcnow() - appointment_datetime).total_seconds() > 86400  # 24 hours
            }
        
        # VIEW APPOINTMENTS
        elif action == 'view_appointments':
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            date_str = data.get('date')
            status = data.get('status', 'upcoming')
            
            query = Appointment.query
            
            # Apply filters based on role
            if role == 'patient':
                query = query.filter_by(patient_id=user_id)
            elif role == 'doctor':
                query = query.filter_by(doctor_id=user_id)
            elif patient_id and ChatbotService._check_permission(role, 'can_view_patients'):
                query = query.filter_by(patient_id=patient_id)
            elif doctor_id and ChatbotService._check_permission(role, 'can_manage_doctors'):
                query = query.filter_by(doctor_id=doctor_id)
            elif not ChatbotService._check_permission(role, 'can_view_all'):
                # Default to own if no permission
                if role == 'patient':
                    query = query.filter_by(patient_id=user_id)
                elif role == 'doctor':
                    query = query.filter_by(doctor_id=user_id)
                else:
                    raise Exception("Not authorized to view appointments")
            
            # Apply date filter
            if date_str:
                query = query.filter_by(date=datetime.strptime(date_str, "%Y-%m-%d").date())
            elif status == 'upcoming':
                query = query.filter(Appointment.date >= datetime.utcnow().date())
            elif status == 'past':
                query = query.filter(Appointment.date < datetime.utcnow().date())
            
            # Apply status filter
            if status != 'all':
                query = query.filter_by(status=status)
            
            appointments = query.order_by(Appointment.date, Appointment.time).limit(20).all()
            
            result = []
            for apt in appointments:
                doctor = Doctor.query.get(apt.doctor_id)
                patient = Patient.query.get(apt.patient_id)
                
                result.append({
                    "id": apt.id,
                    "date": apt.date.strftime("%Y-%m-%d"),
                    "day": apt.date.strftime("%A"),
                    "time": apt.time,
                    "doctor_name": doctor.user.name if doctor else "Unknown",
                    "patient_name": patient.user.name if patient else "Unknown",
                    "status": apt.status,
                    "created_at": apt.created_at.isoformat() if apt.created_at else None
                })
            
            return {
                "appointments": result,
                "count": len(result),
                "filters": {"date": date_str, "status": status}
            }
        
        # SEARCH DOCTORS
        elif action == 'search_doctors':
            department = data.get('department')
            name_query = data.get('name')
            specialization = data.get('specialization')
            
            query = Doctor.query.join(User)
            
            if department:
                query = query.join(Department).filter(Department.name.ilike(f"%{department}%"))
            
            if name_query:
                query = query.filter(User.name.ilike(f"%{name_query}%"))
            
            if specialization:
                query = query.filter(Doctor.specialization.ilike(f"%{specialization}%"))
            
            doctors = query.limit(15).all()
            
            result = []
            for doc in doctors:
                dept = doc.department.name if doc.department else "General"
                result.append({
                    "id": doc.id,
                    "name": doc.user.name,
                    "specialization": doc.specialization,
                    "department": dept,
                    "email": doc.user.email,
                    "phone": doc.user.phone,
                    "availability": "Available" if doc.availability_slots else "By appointment only"
                })
            
            return {
                "doctors": result,
                "count": len(result),
                "search_criteria": {
                    "department": department,
                    "name": name_query,
                    "specialization": specialization
                }
            }
        
        # GET BILLING INFO
        elif action == 'get_billing_info':
            patient_id = data.get('patient_id') or (user_id if role == 'patient' else None)
            
            if not patient_id:
                raise Exception("Patient ID is required")
            
            # Permission check
            if patient_id != user_id and not ChatbotService._check_permission(role, 'can_view_billing'):
                raise Exception("Not authorized to view billing information")
            
            # Get billing records
            bills = Billing.query.filter_by(patient_id=patient_id).order_by(Billing.created_at.desc()).limit(10).all()
            
            total_due = sum(bill.amount_due for bill in bills if bill.status == 'pending')
            total_paid = sum(bill.amount_paid for bill in bills if bill.status == 'paid')
            
            result = []
            for bill in bills:
                result.append({
                    "id": bill.id,
                    "invoice_number": bill.invoice_number,
                    "amount": bill.amount,
                    "amount_paid": bill.amount_paid,
                    "amount_due": bill.amount_due,
                    "status": bill.status,
                    "service_date": bill.service_date.strftime("%Y-%m-%d") if bill.service_date else None,
                    "due_date": bill.due_date.strftime("%Y-%m-%d") if bill.due_date else None,
                    "description": bill.description
                })
            
            return {
                "patient_id": patient_id,
                "bills": result,
                "summary": {
                    "total_due": total_due,
                    "total_paid": total_paid,
                    "outstanding_bills": len([b for b in bills if b.status == 'pending']),
                    "recent_bills": len(bills)
                }
            }
        
        # ESCALATE TO HUMAN
        elif action == 'escalate_to_human':
            if not ChatbotService._check_permission(role, 'can_escalate'):
                raise Exception("Escalation not allowed for your role")
            
            reason = data.get('reason', 'User requested human assistance')
            category = data.get('category', 'general')
            
            # Create escalation ticket
            ticket = EscalationTicket(
                user_id=user_id,
                reason=reason,
                category=category,
                status='open',
                priority=data.get('priority', 'medium'),
                created_at=datetime.utcnow()
            )
            
            db.session.add(ticket)
            db.session.commit()
            
            # Notify admins (placeholder - implement actual notification)
            # notification_service.notify_admins(f"New escalation ticket #{ticket.id}")
            
            return {
                "ticket_id": ticket.id,
                "ticket_number": f"ESC-{ticket.id:06d}",
                "status": "open",
                "created_at": ticket.created_at.isoformat(),
                "estimated_response": "Within 30 minutes",
                "message": "A support agent will contact you shortly."
            }
        
        # UNKNOWN ACTION
        else:
            raise Exception(f"Action '{action}' is not supported")