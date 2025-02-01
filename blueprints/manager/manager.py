from flask import Blueprint
from flask import jsonify, request
from blueprints.database.database import User, Task, db
from datetime import datetime
from roles import role_required
from flask_jwt_extended import get_jwt_identity, jwt_required

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/tasks', methods=['POST'])
@jwt_required()
@role_required('Manager')
def create_task():
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        data = request.get_json()

        if user.role == 'Manager':
            assignee = User.query.filter_by(id=data['assigned_to'], manager_id=user.id).first()

            if not assignee:
                return jsonify({'message': 'Assignee not found'}), 404
            
            new_task = Task(
                title=data['title'],
                description=data['description'],
                due_date=datetime.strptime(data['due_date'], '%d-%m-%y'),
                assigned_to=assignee.id # This is the user ID of the user to whom the task is assigned
            )
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': 'Task created'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to create task', 'error': print(e)}), 500
    
@manager_bp.route('/tasks', methods=['GET'])
@jwt_required()
@role_required('Manager')
def get_tasks():
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'Manager':
            tasks = Task.query.join(User, Task.assigned_to == User.id).filter(User.manager_id == user.id).all()
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
    

@manager_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
@role_required('Manager')
def update_task(task_id):
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        data = request.get_json()
        task = Task.query.filter_by(id=task_id).first()

        if user.role == 'Manager' and task.assigned_to == user.id:
            task.title = data['title']
            task.description = data['description']
            task.due_date = datetime.strptime(data['due_date'], '%d-%m-%y')
            db.session.commit()
            return jsonify({'message': 'Task updated'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed to update task', 'error': print(e)}), 500
    
@manager_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
@role_required('Manager')
def delete_task(task_id):
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        task = Task.query.filter_by(id=task_id).first()

        if user.role == 'Manager' and task.assigned_to == user.id:
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted'}), 200
        else:
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        return jsonify({'message': 'Failed to delete task', 'error': print(e)}), 500