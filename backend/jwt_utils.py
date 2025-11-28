import jwt
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask import request, jsonify, current_app


def generate_token(user_id, role, email, name):
    """
    Generate a JWT token for a user.
    
    Args:
        user_id: User's database ID
        role: User's role (admin, doctor, patient)
        email: User's email
        name: User's name
    
    Returns:
        JWT token string
    """
    secret_key = os.getenv('JWT_SECRET_KEY', current_app.config.get('SECRET_KEY', 'dev-secret-key'))
    expiration = datetime.now(timezone.utc) + timedelta(hours=24)
    
    payload = {
        'user_id': user_id,
        'role': role,
        'email': email,
        'name': name,
        'exp': expiration,
        'iat': datetime.now(timezone.utc)
    }
    
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token


def decode_token(token):
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        Decoded payload dictionary
    
    Raises:
        jwt.ExpiredSignatureError: Token has expired
        jwt.InvalidTokenError: Token is invalid
    """
    secret_key = os.getenv('JWT_SECRET_KEY', current_app.config.get('SECRET_KEY', 'dev-secret-key'))
    
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError('Token has expired')
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError('Invalid token')


def get_current_user():
    """
    Extract current user information from the request token.
    
    Returns:
        Dictionary with user information (user_id, role, email, name)
        None if no valid token found
    """
    auth_header = request.headers.get('Authorization')
    
    if not auth_header:
        return None
    
    try:
        # Expected format: "Bearer <token>"
        token = auth_header.split(' ')[1]
        payload = decode_token(token)
        return payload
    except (IndexError, jwt.InvalidTokenError, jwt.ExpiredSignatureError):
        return None


def token_required(f):
    """
    Decorator to protect endpoints requiring authentication.
    
    Usage:
        @token_required
        def protected_endpoint():
            # Access current user via get_current_user()
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'message': 'Authorization header is missing'}), 401
        
        try:
            # Expected format: "Bearer <token>"
            token = auth_header.split(' ')[1]
            payload = decode_token(token)
            
            # Attach user info to request context
            request.current_user = payload
            
        except IndexError:
            return jsonify({'message': 'Invalid authorization header format'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated


def role_required(*allowed_roles):
    """
    Decorator to protect endpoints requiring specific roles.
    
    Usage:
        @token_required
        @role_required('admin', 'doctor')
        def admin_or_doctor_endpoint():
            pass
    
    Note: Must be used with @token_required decorator
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get current user from request context (set by token_required)
            current_user = getattr(request, 'current_user', None)
            
            if not current_user:
                return jsonify({'message': 'Authentication required'}), 401
            
            user_role = current_user.get('role')
            
            if user_role not in allowed_roles:
                return jsonify({
                    'message': f'Access denied. Required roles: {", ".join(allowed_roles)}'
                }), 403
            
            return f(*args, **kwargs)
        
        return decorated
    
    return decorator
