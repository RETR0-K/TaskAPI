from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from blueprints.database.database import User, Task, db
from roles import role_required
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tasks', methods=['POST'])
@jwt_required()
@role_required('Admin')
def create_task():
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        data = request.get_json()

        if user.role == 'Admin':
            new_task = Task(
                title=data['title'],
                description=data['description'],
                due_date=datetime.strptime(data['due_date'], '%d-%m-%y'),
                assigned_to=data['assigned_to'] # This is the user ID of the user to whom the task is assigned
            )
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': 'Task created'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed to create task', 'error': print(e)}), 500
    
@admin_bp.route('/tasks', methods=['GET'])
@jwt_required()
@role_required('Admin')
def get_tasks():
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'Admin':
            tasks = Task.query.all()
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
    
@admin_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@role_required('Admin')
def delete_task(task_id):
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'Admin':
            task = Task.query.filter_by(id=task_id).first()
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete task', 'error': print(e)}), 500
    
@admin_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
@role_required('Admin')
def update_task(task_id):
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        data = request.get_json()
        if user.role == 'Admin':
            task = Task.query.filter_by(id=task_id).first()
            task.title = data['title']
            task.description = data['description']
            task.status = data['status']
            task.due_date = datetime.strptime(data['due_date'], '%d-%m-%y')
            task.assigned_to = data['assigned_to']
            db.session.commit()
            return jsonify({'message': 'Task updated'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to update task', 'error': print(e)}), 500