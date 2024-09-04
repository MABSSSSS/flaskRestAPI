from flask import Blueprint, request, jsonify
# Importing necessary components from Flask:
# - Blueprint: for modularizing the app.
# - request: to handle incoming request data.
# - jsonify: to return JSON responses.

import validators
# Importing the validators library to validate URLs.

from src.database import Bookmark, db
# Importing the Bookmark model and the database instance from the app's database module.

from flask_jwt_extended import get_jwt_identity
# Importing a function to get the identity (usually user ID) from the JWT.

from flask_jwt_extended.view_decorators import jwt_required
# Importing a decorator to protect routes with JWT authentication.

from src.constants.http_status_codes import OK as HTTP_200_OK, BAD_REQUEST as HTTP_400_BAD_REQUEST, CONFLICT as HTTP_409_CONFLICT, CREATED as HTTP_201_CREATED,  NOT_FOUND as HTTP_404_NOT_FOUND, NO_CONTENT as HTTP_204_NO_CONTENT
# Importing HTTP status codes with custom names for clarity and readability.

from flasgger import swag_from
# Importing swag_from for API documentation generation with Swagger.

# Creating a Blueprint for bookmark-related routes with a URL prefix of '/api/v1/bookmarks'.
bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

# Defining a route that handles both POST and GET requests at the root of the bookmarks Blueprint.
@bookmarks.route('/', methods=['POST', 'GET'])
@jwt_required()
def handle_bookmarks():
    # This route requires JWT authentication.
    
    current_user = get_jwt_identity()
    # Getting the current user's identity (e.g., user ID) from the JWT.
    
    if request.method == 'POST':
        # Handling POST requests to create a new bookmark.
        
        data = request.get_json()
        # Getting the JSON data sent in the request body.
        
        url = data.get('url', '')
        body = data.get('body', '')
        # Extracting the 'url' and 'body' fields from the request data, defaulting to empty strings if not provided.

        if not validators.url(url):
            # Validating the URL. If it's not valid, return an error.
            return jsonify({'error': 'Enter a valid URL'}), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
            # Checking if a bookmark with the same URL already exists for the user.
            return jsonify({'error': 'URL already exists'}), HTTP_409_CONFLICT

        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        # Creating a new Bookmark instance with the provided data and the current user's ID.
        
        db.session.add(bookmark)
        db.session.commit()
        # Adding the new bookmark to the database session and committing the transaction.

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'short_url': bookmark.short_url,
            'visit': bookmark.visits,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at,
        }), HTTP_201_CREATED
        # Returning a JSON response with the created bookmark's details and a 201 Created status.
    
    else:
        # Handling GET requests to retrieve bookmarks.
        
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        # Getting pagination parameters from the query string, with defaults of page 1 and 5 items per page.

        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(page=page, per_page=per_page)
        # Querying the database for bookmarks belonging to the current user and paginating the results.

        data = []
        # Initializing an empty list to store the bookmark data.

        for bookmark in bookmarks.items:
            # Looping through the paginated bookmarks.
            data.append({
                'id': bookmark.id,
                'url': bookmark.url,
                'short_url': bookmark.short_url,
                'visit': bookmark.visits,
                'body': bookmark.body,
                'created_at': bookmark.created_at,
                'updated_at': bookmark.updated_at,
            })
            # Adding each bookmark's details to the data list.

        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev,
        }
        # Creating a metadata dictionary with pagination details.

        return jsonify({'data': data, 'meta': meta}), HTTP_200_OK
        # Returning the bookmark data and pagination metadata as a JSON response with a 200 OK status.

# Defining a route to get a single bookmark by its ID.
@bookmarks.get("/<int:id>")
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    # Getting the current user's identity from the JWT.
    
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    # Querying the database for a bookmark with the specified ID belonging to the current user.

    if not bookmark:
        # If the bookmark doesn't exist, return a 404 Not Found response.
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    }), HTTP_200_OK
    # Returning the bookmark's details as a JSON response with a 200 OK status.

# Defining a route to delete a bookmark by its ID.
@bookmarks.delete("/<int:id>")
@jwt_required()
def delete_bookmark(id):
    current_user = get_jwt_identity()
    # Getting the current user's identity from the JWT.

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    # Querying the database for a bookmark with the specified ID belonging to the current user.

    if not bookmark:
        # If the bookmark doesn't exist, return a 404 Not Found response.
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()
    # Deleting the bookmark from the database and committing the transaction.

    return jsonify({}), HTTP_204_NO_CONTENT
    # Returning an empty JSON response with a 204 No Content status.

# Defining routes to edit (put/patch) a bookmark by its ID.
@bookmarks.put('/<int:id>')
@bookmarks.patch('/<int:id>')
@jwt_required()
def edit_bookmark(id):
    current_user = get_jwt_identity()
    # Getting the current user's identity from the JWT.

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    # Querying the database for a bookmark with the specified ID belonging to the current user.

    if not bookmark:
        # If the bookmark doesn't exist, return a 404 Not Found response.
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND

    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')
    # Getting the 'body' and 'url' fields from the request JSON, defaulting to empty strings if not provided.

    if not validators.url(url):
        # Validating the URL. If it's not valid, return an error.
        return jsonify({'error': 'Enter a valid URL'}), HTTP_400_BAD_REQUEST

    bookmark.url = url 
    bookmark.body = body 
    # Updating the bookmark's URL and body with the new data.

    db.session.commit()
    # Committing the changes to the database.

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'short_url': bookmark.short_url,
        'visit': bookmark.visits,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at,
    }), HTTP_200_OK
    # Returning the updated bookmark's details as a JSON response with a 200 OK status.

# Defining a route to get statistics on all bookmarks.
@bookmarks.get("/stats")
@jwt_required()
@swag_from("./docs/bookmarks/stats.yaml")
# This route is protected with JWT and documented with Swagger using a YAML file.

def get_stats():
    current_user = get_jwt_identity()
    # Getting the current user's identity from the JWT.

    data = []
    # Initializing an empty list to store the statistics data.

    items = Bookmark.query.filter_by(user_id=current_user).all()
    # Querying the database for all bookmarks belonging to the current user.

    for item in items:
        new_link = {
            'visits': item.visits,
            'url': item.url,
            'id': item.id,
            'short_url': item.short_url,
        }
        # Collecting the visit count, URL, ID, and short URL of each bookmark.

        data.append(new_link)
    # Adding each bookmark's statistics to the data list.

    return jsonify({'data': data}), HTTP_200_OK
    # Returning the statistics data as a JSON response with a 200 OK status.
