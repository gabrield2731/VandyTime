from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app

# mongo = current_app.extensions['pymongo']
# classes_collection = mongo.db.classes

def get_class_by_id(class_id):
    """Fetch a class by ID from the MongoDB collection."""
    print("class get")
    return None

def create_class(class_data):
    """Insert a new class into the MongoDB collection."""
    print("class create")
    return None

def update_class(class_id, update_data):
    """Update a class in the MongoDB collection."""
    print("class update", class_id, update_data)
    return None

def delete_class(class_id):
    """Delete a class from the MongoDB collection."""
    print("class delete", class_id)
    return None
