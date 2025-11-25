from backend.celery_config import celery_app
from backend.models import Appointment, Doctor, PatientHistory, Prescription
from backend.app import app
from datetime import datetime, timedelta, timezone
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os


def send_email(to_email, subject, html_content):
    """Helper function to send email"""
    try:
        from_email = os.environ.get('SMTP_EMAIL', 'noreply@hospital.com')
        password = os.environ.get('SMTP_PASSWORD', '')
        smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = from_email
        msg['To'] = to_email
        
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


@celery_app.task(name='backend.tasks.send_daily_reminders')
def send_daily_reminders():
    """Send daily reminders to patients with appointments today"""
    with app.app_context():
        today = datetime.now(timezone.utc).date()
        tomorrow = today + timedelta(days=1)
        
        # Get appointments for today
        appointments = Appointment.query.filter(
            Appointment.status == 'scheduled',
            Appointment.appointment_date >= datetime.combine(today, datetime.min.time()).replace(tzinfo=timezone.utc),
            Appointment.appointment_date < datetime.combine(tomorrow, datetime.min.time()).replace(tzinfo=timezone.utc)
        ).all()
        
        sent_count = 0
        for appt in appointments:
            if appt.patient and appt.patient.user:
                patient_email = appt.patient.user.email
                patient_name = appt.patient.user.name
                doctor_name = appt.doctor.user.name if appt.doctor and appt.doctor.user else 'Your Doctor'
                appt_time = appt.appointment_date.strftime('%I:%M %p')
                
                html_content = f"""
                <html>
                <body style="font-family: Arial, sans-serif; padding: 20px;">
                    <h2 style="color: #6366f1;">Appointment Reminder</h2>
                    <p>Dear {patient_name},</p>
                    <p>This is a reminder that you have an appointment scheduled for <strong>today</strong>.</p>
                    <div style="background-color: #f8fafc; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p><strong>Doctor:</strong> Dr. {doctor_name}</p>
                        <p><strong>Time:</strong> {appt_time}</p>
                        <p><strong>Department:</strong> {appt.department.name if appt.department else 'N/A'}</p>
                    </div>
                    <p>Please arrive 10 minutes before your scheduled time.</p>
                    <p>Best regards,<br>FalcoVita Hospital Team</p>
                </body>
                </html>
                """
                
                if send_email(patient_email, 'Appointment Reminder - Today', html_content):
                    sent_count += 1
        
        return f"Sent {sent_count} reminders"


@celery_app.task(name='backend.tasks.send_monthly_reports')
def send_monthly_reports():
    """Send monthly activity reports to doctors"""
    with app.app_context():
        # Get all doctors
        doctors = Doctor.query.all()
        
        # Calculate previous month date range
        today = datetime.now(timezone.utc)
        first_day_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_day_previous_month = first_day_current_month - timedelta(days=1)
        first_day_previous_month = last_day_previous_month.replace(day=1)
        
        sent_count = 0
        for doctor in doctors:
            if not doctor.user:
                continue
            
            # Get appointments for previous month
            appointments = Appointment.query.filter(
                Appointment.doctor_id == doctor.id,
                Appointment.appointment_date >= first_day_previous_month,
                Appointment.appointment_date <= last_day_previous_month
            ).all()
            
            total_appointments = len(appointments)
            completed = len([a for a in appointments if a.status == 'completed'])
            cancelled = len([a for a in appointments if a.status == 'cancelled'])
            
            # Get treatment details
            histories = PatientHistory.query.filter(
                PatientHistory.doctor_id == doctor.id,
                PatientHistory.visit_date >= first_day_previous_month,
                PatientHistory.visit_date <= last_day_previous_month
            ).all()
            
            # Generate report HTML
            html_content = f"""
            <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f8fafc; }}
                    .container {{ max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 12px; }}
                    h1 {{ color: #6366f1; }}
                    .stats {{ display: flex; gap: 20px; margin: 20px 0; }}
                    .stat-card {{ flex: 1; background-color: #f1f5f9; padding: 20px; border-radius: 8px; }}
                    .stat-number {{ font-size: 32px; font-weight: bold; color: #6366f1; }}
                    table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                    th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #e2e8f0; }}
                    th {{ background-color: #f1f5f9; font-weight: 600; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Monthly Activity Report</h1>
                    <p>Dr. {doctor.user.name}</p>
                    <p>Report Period: {first_day_previous_month.strftime('%B %Y')}</p>
                    
                    <div class="stats">
                        <div class="stat-card">
                            <div class="stat-number">{total_appointments}</div>
                            <div>Total Appointments</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{completed}</div>
                            <div>Completed</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-number">{cancelled}</div>
                            <div>Cancelled</div>
                        </div>
                    </div>
                    
                    <h2>Treatment Summary</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Date</th>
                                <th>Patient</th>
                                <th>Visit Type</th>
                                <th>Diagnosis</th>
                            </tr>
                        </thead>
                        <tbody>
            """
            
            for history in histories[:20]:  # Limit to 20 entries
                patient_name = history.patient.user.name if history.patient and history.patient.user else 'Unknown'
                html_content += f"""
                            <tr>
                                <td>{history.visit_date.strftime('%Y-%m-%d')}</td>
                                <td>{patient_name}</td>
                                <td>{history.visit_type}</td>
                                <td>{history.diagnosis or 'N/A'}</td>
                            </tr>
                """
            
            html_content += """
                        </tbody>
                    </table>
                    
                    <p>Thank you for your dedication to patient care.</p>
                    <p>Best regards,<br>FalcoVita Hospital Administration</p>
                </div>
            </body>
            </html>
            """
            
            if send_email(doctor.user.email, f'Monthly Activity Report - {first_day_previous_month.strftime("%B %Y")}', html_content):
                sent_count += 1
        
        return f"Sent {sent_count} monthly reports"


@celery_app.task(name='backend.tasks.export_patient_history_csv')
def export_patient_history_csv(patient_id):
    """Async task to export patient treatments and send via email"""
    with app.app_context():
        from backend.models import PatientHistory, Prescription, Appointment, Patient
        import csv
        import io
        
        try:
            # Verify patient exists
            patient = Patient.query.filter_by(id=patient_id).first()
            if not patient:
                return f"Patient {patient_id} not found"
            
            if not patient.user or not patient.user.email:
                return f"Patient {patient_id} has no email address"
            
            email = patient.user.email

            # Get all history records
            histories = PatientHistory.query.filter_by(patient_id=patient_id).all()
            
            # Create CSV in memory
            output = io.StringIO()
            writer = csv.writer(output)
            
            # Write header
            writer.writerow([
                'Patient ID',
                'Patient Name',
                'Medical Record Number',
                'Doctor Name',
                'Department',
                'Appointment Date',
                'Visit Type',
                'Diagnosis',
                'Medicines',
                'Dosage',
                'Instructions'
            ])
            
            # Write data
            for history in histories:
                appointment = Appointment.query.filter_by(id=history.appointment_id).first()
                prescriptions = Prescription.query.filter_by(history_id=history.id).all()
                
                # Combine all prescriptions
                medicines = '; '.join([p.medicines for p in prescriptions]) if prescriptions else 'N/A'
                dosages = '; '.join([p.dosage for p in prescriptions]) if prescriptions else 'N/A'
                instructions = '; '.join([p.instructions or '' for p in prescriptions]) if prescriptions else 'N/A'
                
                writer.writerow([
                    patient.id,
                    patient.user.name if patient.user else 'Unknown',
                    patient.medical_record_number,
                    history.doctor.user.name if history.doctor and history.doctor.user else 'Unknown',
                    history.department.name if history.department else 'Unknown',
                    appointment.appointment_date.strftime('%Y-%m-%d %H:%M') if appointment else 'N/A',
                    history.visit_type,
                    history.diagnosis or 'N/A',
                    medicines,
                    dosages,
                    instructions
                ])
            
            csv_content = output.getvalue()
            output.close()
            
            # Prepare Email
            from_email = os.environ.get('SMTP_EMAIL', 'noreply@hospital.com')
            password = os.environ.get('SMTP_PASSWORD', '')
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', '587'))
            
            msg = MIMEMultipart()
            msg['Subject'] = 'Your Treatment History Export'
            msg['From'] = from_email
            msg['To'] = email
            
            html_content = f"""
            <html>
            <body style="font-family: Arial, sans-serif; padding: 20px;">
                <h2 style="color: #6366f1;">Treatment Export Ready</h2>
                <p>Dear {patient.user.name},</p>
                <p>Your treatment history export has been completed and is attached to this email.</p>
                <p>Best regards,<br>FalcoVita Hospital Team</p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html_content, 'html'))
            
            # Attach CSV
            attachment = MIMEText(csv_content, 'csv')
            attachment.add_header('Content-Disposition', 'attachment', filename=f'patient_{patient_id}_history.csv')
            msg.attach(attachment)
            
            # Send Email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, email, msg.as_string())
            server.quit()
            
            return f"Export sent to {email}"
            
        except Exception as e:
            print(f"Export failed: {str(e)}")
            return f"Export failed: {str(e)}"
