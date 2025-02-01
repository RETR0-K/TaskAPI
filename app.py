from config import app
from blueprints.admin.admin import admin_bp
from blueprints.manager.manager import manager_bp
from blueprints.user.user import user_bp
from blueprints.account.account import account_bp
from blueprints.database.database import database_bp, db, User
from flask_migrate import Migrate
from flask import jsonify, redirect, url_for, request
from flask_jwt_extended import get_jwt_identity, jwt_required

all_methods = ['GET', 'POST', 'PUT', 'DELETE']

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(manager_bp, url_prefix='/manager')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(account_bp)
app.register_blueprint(database_bp)

@app.route('/api/<var>', methods=all_methods)
@jwt_required()
def route_to_blueprint(var):
    current_user = User.query.get(get_jwt_identity())

    if current_user.role == 'Admin':
        if request.method == 'POST':
            return redirect(url_for('admin.create_task'), code=307)
        elif request.method == 'GET':
            return redirect(url_for('admin.get_tasks'), code=307)
        elif request.method == 'DELETE':
            return redirect(url_for('admin.delete_task', task_id=var), code=307)
        elif request.method == 'PUT':
            return redirect(url_for('admin.update_task', task_id=var), code=307)
    elif current_user.role == 'Manager':
        if request.method == 'POST':
            return redirect(url_for('manager.create_task'), code=307)
        elif request.method == 'GET':
            return redirect(url_for('manager.get_tasks'), code=307)
        elif request.method == 'PUT':
            return redirect(url_for('manager.update_task', task_id=var), code=307)
        elif request.method == 'DELETE':
            return redirect(url_for('manager.delete_task', task_id=var), code=307)
    elif current_user.role == 'User':
        if request.method == 'GET':
            return redirect(url_for('user.get_tasks'), code=307)
        elif request.method == 'PUT':
            return redirect(url_for('user.update_task', task_id=var), code=307)
    else:
        return jsonify({'error': 'Invalid role'}), 403

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)