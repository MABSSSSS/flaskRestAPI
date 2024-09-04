template = {
    "swagger": "2.0",  # Specifies the version of the Swagger specification being used.
    "info": {  # Information object that provides metadata about the API.
        "title": "Bookmarks API",  # The title of the API.
        "description": "API for bookmarks",  # A brief description of what the API does.
        "contact": {  # Contact information for the responsible party or developer.
            "responsibleOrganization": "",  # Name of the organization responsible for the API.
            "responsibleDeveloper": "",  # Name of the developer responsible for the API.
            "email": "deve@gmail.com",  # Contact email address for the developer or organization.
            "url": "www.twitter.com/deve",  # URL for the developer or organization's website or social media.
        },
        "termsOfService": "www.twitter.com/deve",  # URL for the terms of service for using the API.
        "version": "1.0"  # The current version of the API.
    },
    "basePath": "/api/v1",  # Base path for the API, used in route registration (e.g., "/api/v1/bookmarks").
    "schemes": [
        "http",  # The API can be accessed over HTTP.
        "https"  # The API can also be accessed over HTTPS.
    ],
    "securityDefinitions": {  # Security scheme definitions for the API.
        "Bearer": {  # Name of the security scheme.
            "type": "apiKey",  # Specifies that this scheme is of type `apiKey`.
            "name": "Authorization",  # The name of the header that will contain the API key.
            "in": "header",  # Specifies that the API key should be included in the request header.
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            # Description explaining how the API key should be provided in requests, specifically as a Bearer token.
        }
    },
}

swagger_config = {
    "headers": [
    ],  # Empty list, but could include custom headers for Swagger UI.
    "specs": [  # Specification configuration for the API.
        {
            "endpoint": 'apispec',  # The name of the endpoint that serves the API specification.
            "route": '/apispec.json',  # The route where the API specification can be accessed in JSON format.
            "rule_filter": lambda rule: True,  # Filter to include all routes by returning `True` for any route.
            "model_filter": lambda tag: True,  # Filter to include all models by returning `True` for any tag.
        }
    ],
    "static_url_path": "/flasgger_static",  # The path where static files for Swagger UI will be served.
    "swagger_ui": True,  # Enables or disables the Swagger UI.
    "specs_route": "/"  # The route where the Swagger UI can be accessed.
}
