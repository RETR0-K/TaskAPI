from flask import Flask
from flask_jwt_extended import JWTManager

# Initialize the Flask application
app = Flask(__name__)

# Initialize the JWT manager with the Flask app
jwt = JWTManager(app)

# Configure the SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
# Disable SQLAlchemy event system to save resources
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
# Disable subject verification for JWT
app.config['JWT_VERIFY_SUB'] = False