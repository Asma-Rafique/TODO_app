# TODO App with FastAPI, Async SQLAlchemy, PostgreSQL, and JWT Authentication
## Description
This is a TODO application built with FastAPI, using asynchronous SQLAlchemy for database operations with PostgreSQL. It includes authentication with JWT (JSON Web Tokens) for secure API endpoints.

## Features
- Create, Read, Update, and Delete TODO items
- Pagination for TODO items
- JWT authentication for secure endpoints
- Encrypted responses for added security
## Requirements
- Python 3.9
- PostgreSQL
## Setup Instructions
1. Clone the Repository
2. Create a Virtual Environment
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
3. Install Dependencies
pip install -r requirements.txt
4. Set Up the Database
Make sure PostgreSQL is installed and running on your machine.
5. Create a PostgreSQL database:
CREATE DATABASE todo_database;
CREATE USER postgres WITH PASSWORD 'yourpassword';
GRANT ALL PRIVILEGES ON DATABASE todo_database TO postgres;
6. Run the Application
uvicorn main:app --reload
7. Access the Application
Open your browser and navigate to http://localhost:8000/docs to access the Swagger UI and test the endpoints.

## Endpoints
### Authentication
- Login: POST /token
### TODO Items
- Create TODO: POST /todos/
- Read TODOs: GET /todos/
- Update TODO: PUT /todos/{todo_id}
- Delete TODO: DELETE /todos/{todo_id}
