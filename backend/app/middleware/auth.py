"""Auth middleware for extracting user from JWT token."""
from functools import wraps
from flask import request, jsonify, current_app


def require_auth(f):
    """Decorator to require authentication via Supabase JWT."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            return jsonify({'message': 'Missing authorization token'}), 401
        
        token = auth_header.split(' ')[1]
        try:
            # Verify token with Supabase
            user = current_app.supabase.auth.get_user(token)
            if not user or not user.user:
                return jsonify({'message': 'Invalid token'}), 401
            request.user_id = user.user.id
            request.user = user.user
        except Exception as e:
            return jsonify({'message': f'Authentication failed: {str(e)}'}), 401
        
        return f(*args, **kwargs)
    return decorated
