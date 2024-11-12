from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

def is_valid_objectid(id):
    return ObjectId.is_valid(id)

# Get a student by ID from the MongoDB collection
def get_student_by_id(student_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]

    if not is_valid_objectid(student_id):
        print(f"Error: '{student_id}' is not a valid ObjectId")
        return None

    try:
        student_object = student_collection.find_one({"_id": ObjectId(student_id)})
        return student_object
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return None
    finally:
        client.close()

def get_student_by_fid(student_id):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]

    try:
        student_object = student_collection.find_one({"firebase_id": student_id})
        return student_object
    except Exception as e:
        print(f"Error getting student by ID: {e}")
        return None
    finally:
        client.close()

# Insert a new student into the MongoDB collection
# Student is always inserted with empty classes and grades list
def create_student(student_data):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]

    try:
        if "grades" not in student_data:
            student_data["grades"] = []

        student_object = student_collection.insert_one(student_data)
        return student_object
    except Exception as e:
        print(f"Error inserting student: {e}")
        return None
    finally:
        client.close()

# Update a student by ID in the MongoDB collection
# Cannot update classes or grades lists through this endpoint
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
    from .grade_controller import delete_grade
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    student_collection = db["students"]

    try:
        student_data = get_student_by_id(student_id)

        if not student_data:
            return {"deleted_count": 0}

        student_grades = student_data["grades"]
        for grade_id in student_grades:
            delete_grade(grade_id)
            
        delete_object = student_collection.delete_one({"_id": ObjectId(student_id)})
        return {"deleted_count": delete_object.deleted_count}
    except Exception as e:
        print(f"Error deleting student: {e}")
        return {"error": str(e)}
    finally:
        client.close()
