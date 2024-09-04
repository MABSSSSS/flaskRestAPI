from flask import Flask, redirect, jsonify
import os
from src.auth import auth  # Importing the authentication blueprint from the src.auth module
from src.bookmarks import bookmarks  # Importing the bookmarks blueprint from the src.bookmarks module
from src.database import db, Bookmark  # Importing the database object and the Bookmark model from the src.database module
from flask_jwt_extended import JWTManager  # Importing JWTManager for handling JWT authentication
from http import HTTPStatus  # Importing HTTP status codes for better readability and maintainability
from flasgger import Swagger, swag_from  # Importing Swagger for API documentation and swag_from for linking documentation files
from src.config.swagger import template, swagger_config  # Importing Swagger configuration from the src.config.swagger module

def create_app(test_config=None):
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)  # Create a Flask app instance, allowing relative configuration

    if test_config is None:  # Check if there is no test configuration provided
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),  # Load the secret key from environment variables
            SQLALCHEMY_DATABASE_URI='sqlite:///bookmarks.db',  # Set up the database URI for SQLAlchemy
            SQLALCHEMY_TRACK_MODIFICATIONS=False,  # Disable the modification tracking feature in SQLAlchemy
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),  # Load the JWT secret key from environment variables
            SWAGGER={
                'title': 'Bookmarks API',  # Set the title for the Swagger UI
                'uiversion': 3  # Specify the Swagger UI version
            }
        )
    else:
        app.config.from_mapping(test_config)  # Load the test configuration if provided

    db.init_app(app)  # Initialize the SQLAlchemy database with the Flask app
    JWTManager(app)  # Initialize JWT handling for the app

    app.register_blueprint(auth)  # Register the authentication blueprint with the Flask app
    app.register_blueprint(bookmarks)  # Register the bookmarks blueprint with the Flask app

    Swagger(app, config=swagger_config, template=template)  # Initialize Swagger with custom configuration and template

    @app.get('/<short_url>')  # Define a route to handle GET requests for short URLs
    @swag_from('./docs/short_url.yaml')  # Link the route to its Swagger documentation in the specified YAML file
    def redirect_to_url(short_url):
        """Redirect the user to the real URL based on the provided short URL."""
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()  # Query the Bookmark model for the short URL or return 404 if not found
        bookmark.visits += 1  # Increment the visit count for the bookmark
        db.session.commit()  # Commit the visit count increment to the database
        return redirect(bookmark.url)  # Redirect the user to the original URL associated with the short URL

    @app.errorhandler(HTTPStatus.NOT_FOUND)  # Define a custom error handler for 404 Not Found errors
    def handle_404(e):
        """Return a JSON response for 404 errors."""
        return jsonify({'error': 'Not Found'}), HTTPStatus.NOT_FOUND  # Return a JSON error message and a 404 status code

    @app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)  # Define a custom error handler for 500 Internal Server Error
    def handle_500(e):
        """Return a JSON response for 500 errors."""
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTPStatus.INTERNAL_SERVER_ERROR  # Return a JSON error message and a 500 status code

    return app  # Return the configured Flask app instance
