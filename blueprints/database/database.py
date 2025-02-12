# Database module: Defines database models and initializes SQLAlchemy

from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from config import app

# Initialize blueprint for database operations
database_bp = Blueprint('database', __name__)

# Initialize SQLAlchemy with Flask app
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(80), unique=True, nullable=False)  # Unique username
    password = db.Column(db.String(120), nullable=False)  # User password
    role = db.Column(db.String(20), nullable=False)  # User role (e.g., Admin, Manager, User)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Self-referential foreign key for manager

# Define Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key
    title = db.Column(db.String(120), nullable=False)  # Task title
    description = db.Column(db.String, nullable=False)  # Task description
    status = db.Column(db.String(20), default='Not Started')  # Task status with default value
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Foreign key to User model
    due_date = db.Column(db.Date, nullable=False)  # Task due date
    created_at = db.Column(db.DATETIME, default=datetime.datetime.utcnow)  # Timestamp for task creation
    updated_at = db.Column(db.DATETIME, default=datetime.datetime.utcnow)  # Timestamp for last update