from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Get a student by ID from the MongoDB collection
def get_student_by_id(student_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]
    try:
        student_object = student_collection.find_one({"_id": ObjectId(student_id)})
        return student_object
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return None
    finally:
        client.close()

# Insert a new student into the MongoDB collection
def create_student(student_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]
    try:
        student_object = student_collection.insert_one(student_data)
        return student_object.inserted_id
    except Exception as e:
        print(f"Error inserting student: {e}")
        return None
    finally:
        client.close()

# Update a student by ID in the MongoDB collection
def update_student(student_id, update_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]
    try:
        student_object = student_collection.update_one({"_id": ObjectId(student_id)}, {"$set": update_data})
        return student_object
    except Exception as e:
        print(f"Error updating student: {e}")
        return None
    finally:
        client.close()

# Delete a student by ID from the MongoDB collection
def delete_student(student_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]
    try:
        delete_object = student_collection.delete_one({"_id": ObjectId(student_id)})
        return {"deleted_count": delete_object.deleted_count}
    except Exception as e:
        print(f"Error deleting student: {e}")
        return None
    finally:
        client.close()