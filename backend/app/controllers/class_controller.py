from pymongo import MongoClient
from bson.objectid import ObjectId
from flask import current_app
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Get a class by ID from the MongoDB collection
def get_class_by_id(class_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    class_collection = db["classes"]
    try:
        class_object = class_collection.find_one({"_id": ObjectId(class_id)})
        return class_object
    except Exception as e:
        print(f"Error getting class by ID: {e}")
        return None
    finally:
        client.close()

# Insert a new class into the MongoDB collection
def create_class(class_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    class_collection = db["classes"]
    try:
        from .student_controller import update_student
        class_object = class_collection.insert_one(class_data)
        return class_object.inserted_id
    except Exception as e:
        print(f"Error inserting class: {e}")
        return None
    finally:
        client.close()

# Update a class by ID in the MongoDB collection
# Cannot update the "grades" field through this function unless called by grade
def update_class(class_id, update_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    class_collection = db["classes"]
    try:
        class_object = class_collection.update_one({"_id": ObjectId(class_id)}, {"$set": update_data})
        return class_object
    except Exception as e:
        print(f"Error updating class: {e}")
        return None
    finally:
        client.close()

# Delete a class by ID from the MongoDB collection
def delete_class(class_id):
    from .grade_controller import delete_grade
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    class_collection = db["classes"]
    try:
        class_data = get_class_by_id(class_id)
        class_grades = class_data["grades"]
        for grade_id in class_grades:
            delete_grade(grade_id)
        delete_object = class_collection.delete_one({"_id": ObjectId(class_id)})
        return {"deleted_count": delete_object.deleted_count}
    except Exception as e:
        print(f"Error deleting student: {e}")
        return None
    finally:
        client.close()