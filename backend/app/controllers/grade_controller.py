from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables for MongoDB connection
load_dotenv(find_dotenv())

def process_data(data):
    # Convert ObjectId and other MongoDB-specific types to strings
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, list):
            data[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return data

# Function to establish a MongoDB connection
def get_db_connection():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    return db, client

# Get a grade by ID from the MongoDB collection
def get_grade_by_id(grade_id):
    db, client = get_db_connection()
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
# Ensures the grade ID is updated in the corresponding student and class documents
def create_grade(grade_data):
    db, client = get_db_connection()
    grade_collection = db["grades"]
    student_collection = db["students"]
    class_collection = db["classes"]

    try:
        if "student_id" not in grade_data or "class_id" not in grade_data:
            return None
        
        grade_data["student_id"] = ObjectId(grade_data["student_id"])
        grade_data["class_id"] = ObjectId(grade_data["class_id"])

        grade_object = grade_collection.insert_one(grade_data)

        grade_id = grade_object.inserted_id

        student_collection.update_one(
            {"_id": ObjectId(grade_data['student_id'])},
            {"$push": {"grades": grade_id, "class_ids": grade_data['class_id']}}
        )

        class_collection.update_one(
            {"_id": ObjectId(grade_data['class_id'])},
            {"$push": {"grades": grade_id}}
        )
        
        return grade_id
    except Exception as e:
        print(f"Error inserting grade: {e}")
        return None
    finally:
        client.close()

# Update a grade by ID in the MongoDB collection
def update_grade(grade_id, update_data):
    db, client = get_db_connection()
    grade_collection = db["grades"]

    try:
        # Update the grade document using $set operator
        grade_object = grade_collection.update_one({"_id": ObjectId(grade_id)}, {"$set": update_data})
        return grade_object
    except Exception as e:
        print(f"Error updating grade: {e}")
        return None
    finally:
        client.close()
 
# Delete a grade by ID from the MongoDB collection
# Removes the grade ID from the associated student and class documents
def delete_grade(grade_id):
    db, client = get_db_connection()
    grade_collection = db["grades"]
    student_collection = db["students"]
    class_collection = db["classes"]
    
    try:
        grade_data = get_grade_by_id(grade_id)
        if not grade_data:
            return None

        student_collection.update_one(
            {"_id": ObjectId(grade_data['student_id'])},
            {"$pull": {"grades": ObjectId(grade_id), "class_ids": ObjectId(grade_data['class_id'])}}
        )

        class_collection.update_one(
            {"_id": ObjectId(grade_data['class_id'])},
            {"$pull": {"grades": ObjectId(grade_id)}}
        )

        delete_result = grade_collection.delete_one({"_id": ObjectId(grade_id)})
        return {"deleted_count": delete_result.deleted_count}
    except Exception as e:
        print(f"Error deleting grade: {e}")
        return None
    finally:
        client.close()

# Get all grades for a class in a specific year and semester
def get_grades_by_class(class_id, year, semester):
    db, client = get_db_connection()
    grade_collection = db["grades"]

    try:
        query = {
            "class_id": ObjectId(class_id),
            "year": year,
            "semester": semester.lower()
        }
        
        class_grades_cursor = grade_collection.find(query)

        if grade_collection.count_documents(query) == 0:
            return []

        processed_grades = [process_data(grade) for grade in class_grades_cursor]

        return processed_grades
    except Exception as e:
        print(f"Error getting grades by class: {e}")
        return None
    finally:
        client.close()
