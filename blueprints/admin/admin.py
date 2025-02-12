# Admin Blueprint: Handles task management operations for admins
# Provides endpoints for creating, viewing, updating, and deleting tasks

from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from blueprints.database.database import User, Task, db
from roles import role_required
from datetime import datetime

# Initialize blueprint for admin operations
admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/tasks', methods=['POST'])
@jwt_required()  # Require valid JWT token
@role_required('Admin')  # Restrict to Admin role
def create_task():
    """
    Create a new task.
    Returns:
        JSON message and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current user from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        # Get request data
        data = request.get_json()

        if user.role == 'Admin':
            # Create new task with validated data
            new_task = Task(
                title=data['title'],
                description=data['description'],
                due_date=datetime.strptime(data['due_date'], '%d-%m-%y'),
                assigned_to=data['assigned_to']  # ID of user assigned to task
            )
            # Add and commit new task to database
            db.session.add(new_task)
            db.session.commit()
            return jsonify({'message': 'Task created'}), 200
        else:
            # Return unauthorized if validation fails
            return jsonify({'message': 'Unauthorized'}), 401
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to create task', 'error': print(e)}), 500

@admin_bp.route('/tasks', methods=['GET'])
@jwt_required()  # Require valid JWT token
@role_required('Admin')  # Restrict to Admin role
def get_tasks():
    """
    Retrieve all tasks.
    Returns:
        JSON array of tasks and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current user from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'Admin':
            # Query all tasks
            tasks = Task.query.all()
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

@admin_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()  # Require valid JWT token
@role_required('Admin')  # Restrict to Admin role
def delete_task(task_id):
    """
    Delete a specific task.
    Args:
        task_id: Integer ID of the task to delete
    Returns:
        JSON message and 200 status code on success
        Error message and 500 status code on failure
    """
    try:
        # Get current user from JWT token
        user = User.query.filter_by(id=get_jwt_identity()).first()
        if user.role == 'Admin':
            # Find task by ID
            task = Task.query.filter_by(id=task_id).first()
            # Remove task from database
            db.session.delete(task)
            db.session.commit()
            return jsonify({'message': 'Task deleted'}), 200
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to delete task', 'error': print(e)}), 500

@admin_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()  # Require valid JWT token
@role_required('Admin')  # Restrict to Admin role
def update_task(task_id):
    """
    Update a specific task.
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
        if user.role == 'Admin':
            # Find task by ID
            task = Task.query.filter_by(id=task_id).first()
            # Update task fields with new data
            task.title = data['title']
            task.description = data['description']
            task.status = data['status']
            task.due_date = datetime.strptime(data['due_date'], '%d-%m-%y')
            task.assigned_to = data['assigned_to']
            # Save changes to database
            db.session.commit()
            return jsonify({'message': 'Task updated'}), 200
    except Exception as e:
        # Log error and return 500 response
        return jsonify({'message': 'Failed to update task', 'error': print(e)}), 500