from flask import Blueprint
from flask import jsonify, request
from blueprints.database.database import db, User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

account_bp = Blueprint('account', __name__)


@account_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256', salt_length=16)
        new_user = User(username=data['username'], password=hashed_password, role=data['role'], manager_id=data.get('manager_id'))
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': 'Failed to create a User', 'error': print(e)}), 500
    

@account_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid credentials'}), 401
        access_token = create_access_token(identity=user.id)
        return jsonify({'access token': access_token})
    except Exception as e:
        return jsonify({'message': 'Failed to login', 'error': print(e)}), 500
