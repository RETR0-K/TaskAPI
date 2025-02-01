from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.database.database import User, Task, db

user_bp = Blueprint('user', __name__)

user_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        tasks = Task.query.filter_by(assigned_to=user.id).all()
        return jsonify([{
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'status': task.status,
                'due_date': task.due_date.strftime('%Y-%m-%d'),
                'assigned_to': task.assigned_to
            } for task in tasks]), 200
    except Exception as e:
        return jsonify({'message': 'Failed to retrieve tasks', 'error': print(e)}), 500
    
@user_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        task = Task.query.filter_by(id=task_id).first()
        data = request.get_json()
        
        if task.assigned_to == user.id:
            task.status = data['status']
            db.session.commit()
            return jsonify({'message': 'Task updated'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed to update task', 'error': print(e)}), 500