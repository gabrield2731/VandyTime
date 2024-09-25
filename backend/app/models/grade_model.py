from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app

# mongo = current_app.extensions['pymongo']
# grades_collection = mongo.db.grades

def get_grade_by_id(grade_id):
    """Fetch a grade by ID from the MongoDB collection."""
    print("grade get")
    return None

def create_grade(grade_data):
    """Insert a new grade into the MongoDB collection."""
    print("grade create")
    return None

def update_grade(grade_id, update_data):
    """Update a grade in the MongoDB collection."""
    print("grade update", grade_id, update_data)
    return None

def delete_grade(grade_id):
    """Delete a grade from the MongoDB collection."""
    print("grade delete", grade_id)
    return None
