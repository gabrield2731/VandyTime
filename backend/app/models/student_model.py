from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app

# mongo = current_app.mongo
# students_collection = mongo.db.students

def get_student_by_id(student_id):
    """Fetch a student by ID from the MongoDB collection."""
    print("student get")
    return None

def create_student(student_data):
    """Insert a new student into the MongoDB collection."""
    print("student create")
    return None

def update_student(student_id, update_data):
    print("student update", student_id)
    """Update a student in the MongoDB collection."""
    return None

def delete_student(student_id):
    print("student delete", student_id)
    """Delete a student from the MongoDB collection."""
    return None
