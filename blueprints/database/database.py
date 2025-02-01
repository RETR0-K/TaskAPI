from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
import datetime
from config import app

database_bp = Blueprint('database', __name__)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # This is a self-referential foreign key

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String, nullable=False)
    status = db.Column(db.String(20), default='Not Started') # Not Started, In Progress, Completed
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) 
    due_date = db.Column(db.Date, nullable=False)
    created_at = db.Column(db.DATETIME, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DATETIME, default=datetime.datetime.utcnow)   