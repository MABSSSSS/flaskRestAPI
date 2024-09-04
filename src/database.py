from flask_sqlalchemy import SQLAlchemy
# Importing SQLAlchemy, which is an ORM (Object-Relational Mapper) for interacting with the database.

from enum import unique
# Importing the `unique` decorator from the `enum` module (although it's not used in this code).

from datetime import datetime
# Importing the `datetime` class to handle date and time objects.

import string
# Importing the `string` module to access a collection of string constants like digits and letters.

import random
# Importing the `random` module to generate random values.

db = SQLAlchemy()
# Creating an instance of SQLAlchemy to handle database operations.

class User(db.Model):
    # Defining the `User` model, which represents the `users` table in the database.

    id = db.Column(db.Integer, primary_key=True)
    # Defining the `id` column as an integer and primary key for the `User` table.

    username = db.Column(db.String(80), unique=True, nullable=False)
    # Defining the `username` column as a string (max length 80), which must be unique and not null.

    email = db.Column(db.String(120), unique=True, nullable=False)
    # Defining the `email` column as a string (max length 120), which must be unique and not null.

    password = db.Column(db.Text(), nullable=False)
    # Defining the `password` column to store text (hashed password), which must not be null.

    created_at = db.Column(db.DateTime, default=datetime.now())
    # Defining the `created_at` column to store the timestamp of when the record is created. 
    # It defaults to the current time.

    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    # Defining the `updated_at` column to store the timestamp of when the record is updated.
    # It updates automatically whenever the record is modified.

    bookmarks = db.relationship('Bookmark', backref="user")
    # Creating a relationship with the `Bookmark` model.
    # `backref="user"` adds a `user` attribute to the `Bookmark` model to easily access the associated `User`.

    def __repr__(self) -> str:
        # A special method that defines how the object is represented as a string.
        return f'User>>> {self.username}'
        # When an instance of `User` is printed, it will display as `User>>> username`.

class Bookmark(db.Model):
    # Defining the `Bookmark` model, which represents the `bookmarks` table in the database.

    id = db.Column(db.Integer, primary_key=True)
    # Defining the `id` column as an integer and primary key for the `Bookmark` table.

    body = db.Column(db.Text, nullable=True)
    # Defining the `body` column to store the bookmark's text content. It's optional, so it can be null.

    url = db.Column(db.Text, nullable=False)
    # Defining the `url` column to store the URL of the bookmark. It must not be null.

    short_url = db.Column(db.String(3), nullable=True)
    # Defining the `short_url` column to store a short URL (3 characters). It's optional.

    visits = db.Column(db.Integer, default=0)
    # Defining the `visits` column to store the number of times the bookmark has been visited. 
    # It defaults to 0.

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # Defining the `user_id` column to store the foreign key that references the `id` in the `User` table.

    created_at = db.Column(db.DateTime, default=datetime.now())
    # Defining the `created_at` column to store the timestamp of when the record is created.
    # It defaults to the current time.

    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    # Defining the `updated_at` column to store the timestamp of when the record is updated.
    # It updates automatically whenever the record is modified.

    def generate_short_characters(self):
        # A method to generate a short random string (3 characters) for the short URL.
        
        characters = string.digits + string.ascii_letters
        # Defining a set of characters that includes digits and letters (uppercase and lowercase).

        picked_chars = ''.join(random.choices(characters, k=3))
        # Randomly selecting 3 characters from the defined set to create the short URL.

        link = self.query.filter_by(short_url=picked_chars).first()
        # Checking the database to see if the generated short URL already exists.

        if link:
            # If a bookmark with the generated short URL already exists, recursively call the method again.
            return self.generate_short_characters()
        else:
            # If the short URL is unique, return it.
            return picked_chars

    def __init__(self, **kwargs):
        # The constructor method, called when a new instance of `Bookmark` is created.
        
        super().__init__(**kwargs)
        # Calling the parent class's constructor with the provided arguments.

        self.short_url = self.generate_short_characters()
        # Automatically generating and assigning a short URL to the `short_url` field when a new bookmark is created.

    def __repr__(self) -> str:
        # A special method that defines how the object is represented as a string.
        return f'Bookmark>>> {self.url}'
        # When an instance of `Bookmark` is printed, it will display as `Bookmark>>> url`.
