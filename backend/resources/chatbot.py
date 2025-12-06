# chatbot.py - Enhanced with premium features
from flask import Blueprint, request, jsonify
from flask_security import auth_required, current_user, roles_accepted
from backend.services.chatbot_service import ChatbotService
from backend.extensions import db
import logging

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chatbot')

# Setup logging
logger = logging.getLogger(__name__)

@chatbot_bp.route('/message', methods=['POST'])
@auth_required()
def handle_message():
    """
    Premium message handling with enhanced features
    """
    try:
        data = request.get_json(force=True, silent=True) or {}
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({"error": "Message is required"}), 400
        
        if len(message) > 1000:
            return jsonify({"error": "Message too long (max 1000 characters)"}), 400
        
        # Log message for analytics
        logger.info(f"Chat message from user {current_user.id} ({current_user.role}): {message[:100]}...")
        
        # Process message with premium service
        response = ChatbotService.process_message(current_user.id, message)
        
        if "error" in response:
            return jsonify(response), 404
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": "Please try again later"
        }), 500

@chatbot_bp.route('/execute_action', methods=['POST'])
@auth_required()
def execute_action():
    """
    Execute actions with premium permission checks
    """
    try:
        payload = request.get_json(force=True, silent=True) or {}
        action = payload.get("action")
        data = payload.get("data", {})
        
        if not action:
            return jsonify({"error": "Action is required"}), 400
        
        # Log action execution
        logger.info(f"Action execution: {action} by user {current_user.id}")
        
        # Execute with premium service
        result = ChatbotService.execute_action(current_user.id, action, data)
        
        return jsonify({
            "status": "success",
            "result": result,
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Action execution failed: {str(e)}")
        return jsonify({
            "error": "Action failed",
            "details": str(e),
            "support_code": f"ERR-{int(datetime.utcnow().timestamp())}"
        }), 500

@chatbot_bp.route('/history', methods=['GET'])
@auth_required()
def history():
    """
    Enhanced history with metadata
    """
    try:
        limit = min(int(request.args.get('limit', 20)), 100)  # Cap at 100
        offset = int(request.args.get('offset', 0))
        
        # Get history from service
        history_messages = ChatbotService.get_chat_history(current_user.id, limit=limit)
        
        # Convert to JSON with enhanced metadata
        out = []
        for m in history_messages:
            msg_data = {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at.isoformat() if m.created_at else None,
                "has_action": m.action_data is not None
            }
            
            # Parse action data if exists
            if m.action_data:
                try:
                    msg_data["action"] = json.loads(m.action_data)
                except:
                    msg_data["action"] = None
            
            out.append(msg_data)
        
        # Get conversation summary
        summary = {
            "total_messages": len(history_messages),
            "user_messages": len([m for m in history_messages if m.role == 'user']),
            "assistant_messages": len([m for m in history_messages if m.role == 'assistant']),
            "time_range": {
                "first": out[0]['created_at'] if out else None,
                "last": out[-1]['created_at'] if out else None
            }
        }
        
        return jsonify({
            "messages": out,
            "summary": summary,
            "user": {
                "id": current_user.id,
                "role": current_user.role,
                "name": current_user.name
            }
        }), 200
        
    except Exception as e:
        logger.error(f"History retrieval failed: {str(e)}")
        return jsonify({"error": "Failed to retrieve history"}), 500

@chatbot_bp.route('/suggestions', methods=['GET'])
@auth_required()
def get_suggestions():
    """
    Get role-based suggestions for the user
    """
    try:
        role = current_user.role.lower()
        
        # Role-based quick actions
        suggestions = {
            'admin': [
                {"text": "View today's appointments", "action": "view_appointments", "icon": "📅"},
                {"text": "Check system revenue", "action": "get_reports", "icon": "💰"},
                {"text": "Manage doctors", "action": "search_doctors", "icon": "👨‍⚕️"},
                {"text": "Patient overview", "action": "view_patients", "icon": "👤"}
            ],
            'doctor': [
                {"text": "My schedule today", "action": "view_appointments", "icon": "📋"},
                {"text": "My patients", "action": "view_patients", "icon": "🩺"},
                {"text": "Update availability", "action": "update_availability", "icon": "⏰"},
                {"text": "View medical history", "action": "view_records", "icon": "📄"}
            ],
            'patient': [
                {"text": "Book appointment", "action": "book_appointment", "icon": "📅"},
                {"text": "My appointments", "action": "view_appointments", "icon": "📋"},
                {"text": "Billing info", "action": "get_billing_info", "icon": "💰"},
                {"text": "Find a doctor", "action": "search_doctors", "icon": "🔍"}
            ],
            'receptionist': [
                {"text": "Schedule appointment", "action": "book_appointment", "icon": "📅"},
                {"text": "Check doctor availability", "action": "check_availability", "icon": "⏰"},
                {"text": "Register patient", "action": "register_patient", "icon": "👤"},
                {"text": "View all appointments", "action": "view_appointments", "icon": "📋"}
            ],
            'nurse': [
                {"text": "Assigned patients", "action": "view_patients", "icon": "🩺"},
                {"text": "Today's schedule", "action": "view_appointments", "icon": "📋"},
                {"text": "Update vitals", "action": "update_vitals", "icon": "❤️"},
                {"text": "Medication schedule", "action": "view_medications", "icon": "💊"}
            ]
        }
        
        return jsonify({
            "suggestions": suggestions.get(role, []),
            "role": role,
            "welcome_message": f"Hi {current_user.name}! How can I help you today? 😊"
        }), 200
        
    except Exception as e:
        logger.error(f"Suggestions failed: {str(e)}")
        return jsonify({"error": "Failed to get suggestions"}), 500

@chatbot_bp.route('/clear_history', methods=['POST'])
@auth_required()
def clear_history():
    """
    Clear user's chat history
    """
    try:
        # Delete user's chat messages
        deleted = ChatMessage.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Cleared {deleted} messages",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Clear history failed: {str(e)}")
        return jsonify({"error": "Failed to clear history"}), 500

@chatbot_bp.route('/status', methods=['GET'])
@auth_required()
def bot_status():
    """
    Get chatbot status and capabilities
    """
    role = current_user.role.lower()
    
    capabilities = {
        "can_book_appointments": ChatbotService._check_permission(role, 'can_manage_appointments'),
        "can_view_billing": ChatbotService._check_permission(role, 'can_view_billing'),
        "can_view_reports": ChatbotService._check_permission(role, 'can_view_reports'),
        "can_manage_doctors": ChatbotService._check_permission(role, 'can_manage_doctors'),
        "can_escalate": ChatbotService._check_permission(role, 'can_escalate')
    }
    
    return jsonify({
        "status": "online",
        "system": "FalcoVita AI - Premium Hospital Assistant",
        "version": "2.0.0",
        "user_role": role,
        "capabilities": capabilities,
        "features": [
            "Appointment Management",
            "Doctor Search",
            "Billing Information",
            "Role-based Access",
            "Medical Safety Protocols",
            "Human Escalation",
            "Voice Input Support",
            "Real-time Availability"
        ],
        "support_hours": "24/7",
        "response_time": "< 2 seconds"
    }), 200