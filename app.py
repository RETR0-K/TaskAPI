# Main application file that initializes Flask app and sets up routing logic

# Import Flask app instance and blueprints
from config import app
from blueprints.admin.admin import admin_bp
from blueprints.manager.manager import manager_bp
from blueprints.user.user import user_bp
from blueprints.account.account import account_bp
from blueprints.database.database import database_bp, db, User
from flask_migrate import Migrate
from flask import jsonify, redirect, url_for, request
from flask_jwt_extended import get_jwt_identity, jwt_required

# Define allowed HTTP methods for API endpoints
all_methods = ['GET', 'POST', 'PUT', 'DELETE']

# Register blueprints with their URL prefixes
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(manager_bp, url_prefix='/manager')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(account_bp)
app.register_blueprint(database_bp)

# Main routing endpoint that handles requests based on user role
@app.route('/api/<var>', methods=all_methods)
@jwt_required()  # Requires valid JWT token
def route_to_blueprint(var):
    # Get current user from JWT token
    current_user = User.query.get(get_jwt_identity())

    # Route Admin users to admin blueprint endpoints
    if current_user.role == 'Admin':
        if request.method == 'POST':
            return redirect(url_for('admin.create_task'), code=307)  # 307 preserves HTTP method
        elif request.method == 'GET':
            return redirect(url_for('admin.get_tasks'), code=307)
        elif request.method == 'DELETE':
            return redirect(url_for('admin.delete_task', task_id=var), code=307)
        elif request.method == 'PUT':
            return redirect(url_for('admin.update_task', task_id=var), code=307)
    # Route Manager users to manager blueprint endpoints
    elif current_user.role == 'Manager':
        if request.method == 'POST':
            return redirect(url_for('manager.create_task'), code=307)
        elif request.method == 'GET':
            return redirect(url_for('manager.get_tasks'), code=307)
        elif request.method == 'PUT':
            return redirect(url_for('manager.update_task', task_id=var), code=307)
        elif request.method == 'DELETE':
            return redirect(url_for('manager.delete_task', task_id=var), code=307)
    # Route User users to user blueprint endpoints
    elif current_user.role == 'User':
        if request.method == 'GET':
            return redirect(url_for('user.get_tasks'), code=307) 
        elif request.method == 'PUT':
            return redirect(url_for('user.update_task', task_id=var), code=307)
    else:
        return jsonify({'error': 'Invalid role'}), 403  # Return a 403 error if the role is invalid

# Initialize database migration tool
migrate = Migrate(app, db)

if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)