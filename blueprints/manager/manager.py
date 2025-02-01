# Manager Blueprint: Handles task management operations for managers
# Provides endpoints for creating, viewing, updating, and deleting tasks

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from blueprints.database.database import User, Task, db
from datetime import datetime
from roles import role_required

# Initialize blueprint for manager operations
manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/tasks', methods=['POST'])
@jwt_required()  # Require valid JWT token
@role_required('Manager')  # Restrict to Manager role
def create_task():
    """
    Create a new task assigned to a user managed by the current manager.
    Returns:
        JSON message and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current user from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        # Get request data
        data = request.get_json()

        if user.role == 'Manager':
            # Verify assignee exists and is managed by current manager
            assignee = User.query.filter_by(id=data['assigned_to'], manager_id=user.id).first()

            # Return 404 if assignee not found or not under this manager
            if not assignee:
                return jsonify({'message': 'Assignee not found'}), 404
            
            # Create new task with validated data
            new_task = Task(
                title=data['title'],
                description=data['description'],
                due_date=datetime.strptime(data['due_date'], '%d-%m-%y'),
                assigned_to=assignee.id  # ID of user assigned to task
            )
            # Add and commit new task to database
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': 'Task created'}), 200
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to create task', 'error': print(e)}), 500

@manager_bp.route('/tasks', methods=['GET'])
@jwt_required()  # Require valid JWT token
@role_required('Manager')  # Restrict to Manager role
def get_tasks():
    """
    Retrieve all tasks created by the current manager.
    Returns:
        JSON array of tasks and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current manager from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'Manager':
            # Query tasks assigned by the current manager
            tasks = Task.query.join(User, Task.assigned_to == User.id).filter(User.manager_id == user.id).all()
            # Format tasks for JSON response
            return jsonify([{
                    'id': task.id,
                    'title': task.title,
                    'description': task.description,
                    'status': task.status,
                    'due_date': task.due_date.strftime('%Y-%m-%d'),
                    'assigned_to': task.assigned_to
                } for task in tasks]), 200
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to retrieve tasks', 'error': print(e)}), 500

@manager_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()  # Require valid JWT token
@role_required('Manager')  # Restrict to Manager role
def update_task(task_id):
    """
    Update a specific task assigned to the manager.
    Args:
        task_id: Integer ID of the task to update
    Returns:
        JSON message and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current user from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        # Get request data
        data = request.get_json()
        # Find task by ID
        task = Task.query.filter_by(id=task_id).first()

        # Verify user is Manager and owns the task
        if user.role == 'Manager' and task.assigned_to == user.id:
            # Update task fields with new data
            task.title = data['title']
            task.description = data['description']
            task.due_date = datetime.strptime(data['due_date'], '%d-%m-%y')
            # Save changes to database
            db.session.commit()
            return jsonify({'message': 'Task updated'}), 200
        else:
            # Return unauthorized if validation fails
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to update task', 'error': print(e)}), 500

@manager_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()  # Require valid JWT token
@role_required('Manager')  # Restrict to Manager role
def delete_task(task_id):
    """
    Delete a specific task assigned to the manager.
    Args:
        task_id: Integer ID of the task to delete
    Returns:
        JSON message and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current user from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        # Find task by ID
        task = Task.query.filter_by(id=task_id).first()

        # Verify user is Manager and owns the task
        if user.role == 'Manager' and task.assigned_to == user.id:
            # Remove task from database
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted'}), 200
        else:
            # Return unauthorized if validation fails
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to delete task', 'error': print(e)}), 500