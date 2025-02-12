# Task Management API

## Overview
This project is a Task Management API built with Flask. It provides endpoints for managing tasks, including creating, viewing, updating, and deleting tasks. The API supports different user roles (Admin, Manager, User) with role-based access control.

## Features
- User registration and login with JWT authentication
- Role-based access control for Admin, Manager, and User roles
- Task management operations (create, view, update, delete)
- Database models for User and Task using SQLAlchemy
- Blueprint structure for modular code organization

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/TaskAPI.git
    cd TaskAPI
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the database:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Configuration
Edit the `config.py` file to configure the database URI and JWT settings.

## Running the Application
Start the Flask application:
```sh
flask run
```

## API Endpoints

### Account Endpoints
- `POST /register`: Register a new user
- `POST /login`: Login a user and return an access token

### User Endpoints
- `GET /api/tasks`: Retrieve all tasks assigned to the current user
- `PUT /api/<int:task_id>`: Update the status of a specific task assigned to the user

### Manager Endpoints
- `POST /api/tasks`: Create a new task assigned to a user managed by the current manager
- `GET /api/tasks`: Retrieve all tasks created by the current manager
- `PUT /api/<int:task_id>`: Update a specific task assigned to the manager
- `DELETE /api/<int:task_id>`: Delete a specific task assigned to the manager

### Admin Endpoints
- `POST /api/tasks`: Create a new task
- `GET /api/tasks`: Retrieve all tasks
- `PUT /api/<int:task_id>`: Update a specific task
- `DELETE /api/<int:task_id>`: Delete a specific task

## License
This project is licensed under the MIT License.