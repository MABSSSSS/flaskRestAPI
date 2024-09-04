from flask import Flask
from flask_jwt_extended import JWTManager  # Importing JWTManager to handle JWT-based authentication
from flasgger import Swagger  # Importing Swagger to generate and serve API documentation
from src.auth import auth  # Importing the authentication blueprint from the src.auth module
from src.bookmarks import bookmarks  # Importing the bookmarks blueprint from the src.bookmarks module
from src.config.swagger import template, swagger_config  # Importing Swagger configuration and template

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__)  # Create a Flask app instance

    # Initialize Swagger with custom configuration and template
    Swagger(app, config=swagger_config, template=template)  # Integrating Swagger for API documentation

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Set the secret key for JWT. This should be set to a secure, unpredictable value
    jwt = JWTManager(app)  # Initialize JWTManager with the Flask app to enable JWT handling

    # Register Blueprints
    app.register_blueprint(auth)  # Register the authentication blueprint with the app
    app.register_blueprint(bookmarks)  # Register the bookmarks blueprint with the app

    # Other configurations if necessary...
    # You can add more configuration settings or components initialization here

    return app  # Return the configured Flask app instance
