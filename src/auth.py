from flask import Blueprint, request, jsonify  # Import Flask components for Blueprint, handling requests, and returning JSON responses
from werkzeug.security import check_password_hash, generate_password_hash  # Import functions for password hashing and verification
from src.constants.http_status_codes import (  # Import HTTP status codes with custom aliases for readability
    BAD_REQUEST as HTTP_400_BAD_REQUEST,  # HTTP 400: Bad Request, used for invalid requests
    CONFLICT as HTTP_409_CONFLICT,  # HTTP 409: Conflict, used when resources conflict, e.g., duplicate username/email
    CREATED as HTTP_201_CREATED,  # HTTP 201: Created, used when a resource is successfully created
    UNAUTHORIZED as HTTP_401_UNAUTHORIZED,  # HTTP 401: Unauthorized, used for failed authentication
    OK as HTTP_200_OK,  # HTTP 200: OK, used for successful requests
    NOT_FOUND as HTTP_404_NOT_FOUND  # HTTP 404: Not Found, used when a resource is not found
)
import validators  # Import the validators module for input validation (e.g., email validation)
from src.database import User, db  # Import User model and database instance from the database module
from flask_jwt_extended import jwt_required, create_access_token, create_refresh_token, get_jwt_identity  # Import JWT handling functions for authentication
from flasgger import swag_from  # Import swag_from to link Swagger documentation to API routes

# Create a Blueprint for authentication routes, with a URL prefix for all routes in this Blueprint
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

@auth.post('/register')
@swag_from('./docs/auth/register.yaml')  # Link Swagger documentation to the register endpoint
def register():
    """Register a new user."""
    
    # Ensure that the request content type is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), HTTP_400_BAD_REQUEST

    data = request.get_json()  # Parse JSON data from the request body
    username = data.get('username')  # Extract username from the request data
    email = data.get('email')  # Extract email from the request data
    password = data.get('password')  # Extract password from the request data

    # Validate input fields for completeness
    if not username or not email or not password:
        return jsonify({'error': 'Missing required fields'}), HTTP_400_BAD_REQUEST

    # Validate password length (minimum 6 characters)
    if len(password) < 6:
        return jsonify({'error': 'Password is too short'}), HTTP_400_BAD_REQUEST

    # Validate username length (minimum 3 characters)
    if len(username) < 3:
        return jsonify({'error': 'Username is too short'}), HTTP_400_BAD_REQUEST

    # Validate username (alphanumeric and no spaces allowed)
    if not username.isalnum() or " " in username:
        return jsonify({'error': 'Username should be alphanumeric and contain no spaces'}), HTTP_400_BAD_REQUEST

    # Validate email format using the validators module
    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST

    # Check if the email is already taken by another user
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email is already taken'}), HTTP_409_CONFLICT

    # Check if the username is already taken by another user
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username is already taken'}), HTTP_409_CONFLICT

    # Hash the user's password for security purposes
    pwd_hash = generate_password_hash(password)
    # Create a new User instance with the provided username, hashed password, and email
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)  # Add the new user to the database session
    db.session.commit()  # Commit the transaction to save the user to the database

    # Return a success message along with the created user's username and email
    return jsonify({
        'message': "User Created",
        'user': username,
        'email': email
    }), HTTP_201_CREATED  # Respond with HTTP 201: Created

@auth.post('/login')
@swag_from('./docs/auth/login.yaml')  # Link Swagger documentation to the login endpoint
def login():
    """Authenticate a user and return JWT tokens."""
    
    # Ensure that the request content type is JSON
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), HTTP_400_BAD_REQUEST

    data = request.get_json()  # Parse JSON data from the request body
    email = data.get('email')  # Extract email from the request data
    password = data.get('password')  # Extract password from the request data

    # Find the user in the database by email
    user = User.query.filter_by(email=email).first()

    # Verify if the user exists and if the provided password matches the stored hashed password
    if user and check_password_hash(user.password, password):
        # Create a refresh token and an access token for the authenticated user
        refresh = create_refresh_token(identity=user.id)
        access = create_access_token(identity=user.id)

        # Return the tokens and user details
        return jsonify({
            'user': {
                'refresh': refresh,
                'access': access,
                'username': user.username,
                'email': user.email
            }
        }), HTTP_200_OK  # Respond with HTTP 200: OK

    # If authentication fails, return an error message
    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED  # Respond with HTTP 401: Unauthorized

@auth.get("/me")
@jwt_required()  # Protect this route with JWT authentication
def me():
    """Return information about the currently authenticated user."""
    
    user_id = get_jwt_identity()  # Get the authenticated user's ID from the JWT
    user = User.query.filter_by(id=user_id).first()  # Find the user by their ID in the database

    # If the user is found, return their username and email
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email
        }), HTTP_200_OK  # Respond with HTTP 200: OK

    # If the user is not found, return an error message
    return jsonify({'error': 'User not found'}), HTTP_404_NOT_FOUND  # Respond with HTTP 404: Not Found

@auth.post('/token/refresh')
@jwt_required(refresh=True)  # Require a valid refresh token to access this route
def refresh_users_token():
    """Refresh the access token for the currently authenticated user."""
    
    identity = get_jwt_identity()  # Get the authenticated user's ID from the JWT
    access = create_access_token(identity=identity)  # Create a new access token

    # Return the new access token
    return jsonify({
        'access': access
    }), HTTP_200_OK  # Respond with HTTP 200: OK
