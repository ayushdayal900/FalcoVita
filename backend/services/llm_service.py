# backend/services/llm_service.py (new file)
import json
import re
from typing import Dict, Any, Optional
from datetime import datetime

class LLMService:
    """
    Premium LLM Service for FalcoVita AI
    Simulates intelligent responses with role-based behavior
    """
    
    # System prompt for FalcoVita AI
    SYSTEM_PROMPT = """You are FalcoVita AI, the intelligent conversational assistant inside the FalcoVita Hospital Management System.

    🎯 CORE RESPONSIBILITIES:
    1. Hospital Operations: Appointments, doctor info, patient summaries, scheduling, billing, reports
    2. Navigation Help: Guide users through FalcoVita UI modules
    3. Action Triggering: Output structured JSON actions for backend execution

    👥 ROLE-BASED BEHAVIOR:
    - ADMIN: Full access to everything
    - DOCTOR: Own schedule, assigned patients only
    - RECEPTIONIST/STAFF: Manage appointments, register patients
    - PATIENT: Own appointments, booking, basic info
    - NURSE: Assigned patients, vitals, schedules

    🗣️ COMMUNICATION STYLE:
    - Friendly, warm, professional 😊
    - Short paragraphs, simple language
    - 1-2 emojis max
    - Never robotic, never say "As an AI"

    🛑 MEDICAL SAFETY RULES:
    - NEVER give diagnosis or treatment advice
    - For urgent symptoms: "Contact medical professional immediately"
    - Only explain general concepts

    🛠️ ACTION OUTPUT FORMAT:
    Always respond with natural language + optional JSON action:
    {
      "action": "action_name",
      "data": { "field": "value" }
    }

    🧩 CHOICE BUTTONS:
    When helpful, provide choices:
    {
      "action": "choices",
      "data": { "options": ["Option 1", "Option 2"] }
    }

    ❌ REFUSAL POLICY:
    If unauthorized: "I'm not allowed to access that with your current permissions."
    """

    @staticmethod
    def generate_premium_response(message: str, user_role: str, user_id: int, 
                                 context: str, history: str, user_info: str) -> Dict[str, Any]:
        """
        Generate intelligent response with role-appropriate actions
        """
        # Clean and analyze message
        message_lower = message.lower().strip()
        
        # Extract intent
        intent = LLMService._detect_intent(message, user_role)
        
        # Generate appropriate response
        response = LLMService._generate_response_by_intent(intent, message, user_role, context)
        
        return response
    
    @staticmethod
    def _detect_intent(message: str, user_role: str) -> str:
        """Detect user intent from message"""
        message_lower = message.lower()
        
        # Appointment related
        if any(word in message_lower for word in ['book', 'appointment', 'schedule', 'meet']):
            return 'book_appointment'
        if any(word in message_lower for word in ['cancel', 'reschedule', 'postpone']):
            return 'cancel_appointment'
        if any(word in message_lower for word in ['availability', 'available', 'free', 'slot']):
            return 'check_availability'
        if any(word in message_lower for word in ['appointments', 'schedule', 'calendar']):
            return 'view_appointments'
        
        # Doctor related
        if any(word in message_lower for word in ['doctor', 'dr.', 'physician', 'specialist']):
            return 'search_doctors'
        if any(word in message_lower for word in ['department', 'cardiology', 'orthopedic', 'pediatric']):
            return 'search_department'
        
        # Patient related
        if any(word in message_lower for word in ['patient', 'medical history', 'record']):
            return 'view_patient'
        
        # Billing related
        if any(word in message_lower for word in ['bill', 'invoice', 'payment', 'fee', 'cost']):
            return 'billing_info'
        
        # Reports (admin only)
        if any(word in message_lower for word in ['report', 'analytics', 'revenue', 'statistics']):
            return 'view_reports'
        
        # Navigation help
        if any(word in message_lower for word in ['how to', 'where is', 'navigate', 'find']):
            return 'navigation_help'
        
        # Emergency/medical (safety check)
        if any(word in message_lower for word in ['emergency', 'urgent', 'pain', 'symptom', 'diagnose']):
            return 'medical_safety'
        
        # General help
        if any(word in message_lower for word in ['help', 'assist', 'support', 'what can you do']):
            return 'general_help'
        
        # Escalation
        if any(word in message_lower for word in ['human', 'agent', 'representative', 'talk to person']):
            return 'escalate'
        
        return 'general_inquiry'
    
    @staticmethod
    def _generate_response_by_intent(intent: str, message: str, user_role: str, context: str) -> Dict[str, Any]:
        """Generate response based on intent and role"""
        
        # MEDICAL SAFETY - Highest priority
        if intent == 'medical_safety':
            return {
                "text": "🚨 **Important Medical Notice** 🚨\n\nI'm not a medical professional. If you're experiencing urgent symptoms or need medical advice, please:\n\n1. **Contact your doctor immediately**\n2. **Call emergency services** if it's life-threatening\n3. **Visit the nearest hospital**\n\nI can only help with appointment scheduling and hospital administrative tasks.",
                "action": {
                    "action": "escalate_to_human",
                    "data": {
                        "reason": "User mentioned medical symptoms/emergency",
                        "priority": "high",
                        "category": "medical_safety"
                    }
                }
            }
        
        # BOOK APPOINTMENT
        elif intent == 'book_appointment':
            # Extract details
            doctor_name = LLMService._extract_entity(message, 'doctor')
            date = LLMService._extract_entity(message, 'date')
            time_pref = LLMService._extract_entity(message, 'time')
            
            response_text = "Sure! Let's book your appointment. "
            
            if not doctor_name:
                response_text += "Which doctor would you like to see? "
            if not date:
                response_text += "When would you prefer? "
            
            response_text += "😊"
            
            action_data = {}
            if doctor_name:
                action_data['doctor_name'] = doctor_name
            if date:
                action_data['date'] = date
            if time_pref:
                action_data['preferred_time'] = time_pref
            
            if action_data:
                return {
                    "text": response_text,
                    "action": {
                        "action": "check_availability",
                        "data": action_data
                    }
                }
            else:
                # Provide choices if no details
                return {
                    "text": "I can help you book an appointment! 😊\n\nWould you like to:",
                    "action": {
                        "action": "choices",
                        "data": {
                            "options": [
                                "Check doctor availability",
                                "Book with my regular doctor",
                                "Find a specialist",
                                "See available slots this week"
                            ]
                        }
                    }
                }
        
        # CHECK AVAILABILITY
        elif intent == 'check_availability':
            doctor_name = LLMService._extract_entity(message, 'doctor')
            date = LLMService._extract_entity(message, 'date')
            time_pref = LLMService._extract_entity(message, 'time')
            
            response_text = "Checking availability for you..."
            
            if doctor_name:
                response_text = f"Checking availability for Dr. {doctor_name}..."
            elif 'department' in message.lower():
                dept = LLMService._extract_entity(message, 'department')
                if dept:
                    response_text = f"Finding available doctors in {dept.title()}..."
            
            action_data = {}
            if doctor_name:
                action_data['doctor_name'] = doctor_name
            elif 'department' in message.lower():
                dept = LLMService._extract_entity(message, 'department')
                if dept:
                    action_data['department'] = dept
            
            if date:
                action_data['date'] = date
            if time_pref:
                action_data['preferred_time'] = time_pref
            
            return {
                "text": response_text + " 📅",
                "action": {
                    "action": "check_availability",
                    "data": action_data
                }
            }
        
        # CANCEL APPOINTMENT
        elif intent == 'cancel_appointment':
            response_text = "I can help you cancel an appointment. "
            
            # Check if specific appointment mentioned
            if '#' in message or 'id' in message.lower():
                return {
                    "text": "Cancelling the specified appointment...",
                    "action": {
                        "action": "cancel_appointment",
                        "data": {}
                    }
                }
            else:
                return {
                    "text": "Which appointment would you like to cancel? You can tell me the doctor's name, date, or appointment ID.",
                    "action": {
                        "action": "view_appointments",
                        "data": {"status": "upcoming"}
                    }
                }
        
        # VIEW APPOINTMENTS
        elif intent == 'view_appointments':
            if user_role == 'patient':
                response_text = "Showing your upcoming appointments... 📋"
                action_type = "view_appointments"
                action_data = {"patient_id": "current", "status": "upcoming"}
            elif user_role == 'doctor':
                response_text = "Showing your schedule for today... 🩺"
                action_type = "view_appointments"
                action_data = {"doctor_id": "current", "status": "upcoming"}
            else:
                response_text = "Showing appointments... 📅"
                action_type = "view_appointments"
                action_data = {"status": "today"}
            
            return {
                "text": response_text,
                "action": {
                    "action": action_type,
                    "data": action_data
                }
            }
        
        # SEARCH DOCTORS
        elif intent == 'search_doctors' or intent == 'search_department':
            doctor_name = LLMService._extract_entity(message, 'doctor')
            department = LLMService._extract_entity(message, 'department')
            
            if department:
                response_text = f"Finding doctors in {department.title()}... 🏥"
                action_data = {"department": department}
            elif doctor_name:
                response_text = f"Searching for Dr. {doctor_name}... 🔍"
                action_data = {"name": doctor_name}
            else:
                response_text = "I can help you find a doctor. Which department or specialty?"
                return {
                    "text": response_text,
                    "action": {
                        "action": "choices",
                        "data": {
                            "options": [
                                "Cardiology (Heart)",
                                "Orthopedics (Bones)",
                                "Pediatrics (Children)",
                                "Neurology (Brain)",
                                "Find by name"
                            ]
                        }
                    }
                }
            
            return {
                "text": response_text,
                "action": {
                    "action": "search_doctors",
                    "data": action_data
                }
            }
        
        # BILLING INFO
        elif intent == 'billing_info':
            if user_role == 'patient':
                response_text = "Showing your billing information... 💰"
                action_data = {"patient_id": "current"}
            elif user_role == 'admin':
                response_text = "Showing billing overview... 📊"
                action_data = {}
            else:
                response_text = "I can check billing information. Please provide the patient name or ID."
                return {
                    "text": response_text,
                    "action": None
                }
            
            return {
                "text": response_text,
                "action": {
                    "action": "get_billing_info",
                    "data": action_data
                }
            }
        
        # ESCALATE TO HUMAN
        elif intent == 'escalate':
            return {
                "text": "I'm connecting you with a human representative. One moment please... 👤",
                "action": {
                    "action": "escalate_to_human",
                    "data": {
                        "reason": "User requested human assistance",
                        "priority": "medium"
                    }
                }
            }
        
        # NAVIGATION HELP
        elif intent == 'navigation_help':
            navigation_tips = {
                'appointments': "Go to **Appointments** → **Schedule** in the left sidebar.",
                'doctors': "Click **Doctors** → **Manage Doctors** to view all doctors.",
                'patients': "Navigate to **Patients** → **Records** to access patient data.",
                'billing': "Find billing in **Finance** → **Billing & Invoices**.",
                'reports': "Admin reports are in **Analytics** → **Reports**."
            }
            
            for key, tip in navigation_tips.items():
                if key in message.lower():
                    return {
                        "text": f"To access {key.title()}:\n\n{tip}\n\nNeed more specific guidance?",
                        "action": None
                    }
            
            return {
                "text": "I can guide you through FalcoVita! Which section do you need help with?",
                "action": {
                    "action": "choices",
                    "data": {
                        "options": [
                            "Appointments & Scheduling",
                            "Doctor Management",
                            "Patient Records",
                            "Billing & Payments",
                            "Reports & Analytics"
                        ]
                    }
                }
            }
        
        # GENERAL HELP
        elif intent == 'general_help':
            role_based_help = {
                'admin': "I can help with: System reports, doctor management, patient overviews, billing analytics, and appointment scheduling.",
                'doctor': "I can show: Your schedule, patient visits, availability updates, and appointment management.",
                'patient': "I can assist with: Booking appointments, viewing your schedule, checking bills, and finding doctors.",
                'receptionist': "I can help: Schedule appointments, register patients, check doctor availability, and manage bookings.",
                'nurse': "I can show: Assigned patients, schedules, vitals tracking, and appointment information."
            }
            
            help_text = role_based_help.get(user_role, "I can help with hospital management tasks!")
            
            return {
                "text": f"Hi! I'm FalcoVita AI, your hospital assistant. 😊\n\n{help_text}\n\nWhat would you like to do?",
                "action": {
                    "action": "choices",
                    "data": {
                        "options": [
                            "Book an appointment",
                            "Check availability",
                            "View appointments",
                            "Find a doctor",
                            "Billing information",
                            "Get navigation help"
                        ]
                    }
                }
            }
        
        # DEFAULT: General inquiry
        else:
            return {
                "text": "I'm here to help with hospital management tasks! 😊\n\nYou can ask me to book appointments, check doctor availability, view schedules, or get billing information. What would you like to do?",
                "action": {
                    "action": "choices",
                    "data": {
                        "options": [
                            "What can you help me with?",
                            "Book an appointment",
                            "Check doctor availability",
                            "View my schedule",
                            "Find a specialist"
                        ]
                    }
                }
            }
    
    @staticmethod
    def _extract_entity(text: str, entity_type: str) -> Optional[str]:
        """Extract entities from text"""
        if entity_type == 'doctor':
            # Match Dr. Name or Doctor Name
            match = re.search(r'(?:dr\.?|doctor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            
            # Match "with Dr. Name" pattern
            match = re.search(r'with\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        elif entity_type == 'date':
            # Tomorrow
            if 'tomorrow' in text.lower():
                return 'tomorrow'
            # Weekdays
            weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            for day in weekdays:
                if day in text.lower():
                    return day
            # Date patterns
            match = re.search(r'\b(\d{4}-\d{2}-\d{2})\b', text)
            if match:
                return match.group(1)
            match = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b', text)
            if match:
                return f"{match.group(3)}-{match.group(1).zfill(2)}-{match.group(2).zfill(2)}"
        
        elif entity_type == 'time':
            # Morning/Afternoon/Evening
            if 'morning' in text.lower():
                return 'morning'
            if 'afternoon' in text.lower():
                return 'afternoon'
            if 'evening' in text.lower():
                return 'evening'
            # Specific times
            match = re.search(r'\b(\d{1,2})(?::(\d{2}))?\s*(am|pm)?\b', text.lower())
            if match:
                return match.group(0)
        
        elif entity_type == 'department':
            departments = {
                'cardiology': ['cardio', 'heart'],
                'orthopedics': ['ortho', 'bone'],
                'pediatrics': ['pediatric', 'child', 'kids'],
                'neurology': ['neuro', 'brain'],
                'dermatology': ['derm', 'skin'],
                'gastroenterology': ['gastro', 'stomach'],
                'oncology': ['onco', 'cancer'],
                'psychiatry': ['psych', 'mental']
            }
            
            text_lower = text.lower()
            for dept, keywords in departments.items():
                if any(keyword in text_lower for keyword in [dept] + keywords):
                    return dept
        
        return None
    
    @staticmethod
    def generate_response(message, role, context, history_text):
        """Legacy method for compatibility"""
        return LLMService.generate_premium_response(
            message=message,
            user_role=role,
            user_id=0,
            context=context,
            history=history_text,
            user_info=f"Role: {role}"
        )