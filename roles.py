from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.database.database import User  # Adjust the import based on your project structure

def role_required(*roles):
    def wrapper(func):
        @jwt_required()
        def wrapped(*args, **kwargs):
            current_user = User.query.get(get_jwt_identity())
            if current_user.role not in roles:
                return jsonify({'error': 'Unauthorized'}), 403
            return func(*args, **kwargs)
        wrapped.__name__ = func.__name__
        return wrapped
    return wrapper
