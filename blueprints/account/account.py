# Account Blueprint: Handles user registration and login operations

from flask import Blueprint
from flask import jsonify, request
from blueprints.database.database import db, User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize blueprint for account operations
account_bp = Blueprint('account', __name__)

@account_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Returns:
        JSON message and 201 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get request data
        data = request.get_json()
        # Hash the user's password
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
        # Create new user with hashed password
        new_user = User(username=data['username'], password=hashed_password, role=data['role'], manager_id=data.get('manager_id'))
        # Add and commit new user to database
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to create a User', 'error': print(e)}), 500

@account_bp.route('/login', methods=['POST'])
def login():
    """
    Login a user and return an access token.
    Returns:
        JSON access token and 200 status code on success
        Error message and 401 status code on failure
    """
    try:
        # Get request data
        data = request.get_json()
        # Query user by username
        user = User.query.filter_by(username=data['username']).first()
        # Verify password
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        # Create access token for user
        access_token = create_access_token(identity=user.id)
        return jsonify({'access token': access_token})
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to login', 'error': print(e)}), 500
