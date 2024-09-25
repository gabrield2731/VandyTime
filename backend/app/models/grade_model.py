from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Get a grade by ID from the MongoDB collection
def get_grade_by_id(grade_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    grade_collection = db["grades"]
    try:
        grade_object = grade_collection.find_one({"_id": ObjectId(grade_id)})
        return grade_object
    except Exception as e:
        print(f"Error getting grade by ID: {e}")
        return None
    finally:
        client.close()

# Insert a new grade into the MongoDB collection
def create_grade(grade_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    grade_collection = db["grades"]
    try:
        grade_object = grade_collection.insert_one(grade_data)
        return grade_object.inserted_id
    except Exception as e:
        print(f"Error inserting grade: {e}")
        return None
    finally:
        client.close()

# Update a grade by ID in the MongoDB collection
def update_grade(grade_id, update_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    grade_collection = db["grades"]
    try:
        grade_object = grade_collection.update_one({"_id": ObjectId(grade_id)}, {"$set": update_data})
        return grade_object
    except Exception as e:
        print(f"Error updating grade: {e}")
        return None
    finally:
        client.close()

# Delete a grade by ID from the MongoDB collection
def delete_grade(grade_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    grade_collection = db["grades"]
    try:
        delete_object = grade_collection.delete_one({"_id": ObjectId(grade_id)})
        return {"deleted_count": delete_object.deleted_count}
    except Exception as e:
        print(f"Error updating grade: {e}")
        return None
    finally:
        client.close()