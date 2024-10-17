from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables for MongoDB connection
load_dotenv(find_dotenv())

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
        # Insert the grade into the grades collection
        grade_object = grade_collection.insert_one(grade_data)

        # Get the inserted grade ID
        grade_id = grade_object.inserted_id

        student_update_result = student_collection.update_one(
            {"_id": ObjectId(grade_data['student_id'])},
            {"$push": {"grades": grade_id}}
        )

        # Use $push to add the grade ID to the class's grades array
        class_update_result = class_collection.update_one(
            {"_id": ObjectId(grade_data['class_id'])},
            {"$push": {"grades": grade_id}}
        )

        # Check if the updates were successful
        if student_update_result.modified_count == 0:
            print(f"Failed to update student {grade_data['student_id']} with the new grade.")
        if class_update_result.modified_count == 0:
            print(f"Failed to update class {grade_data['class_id']} with the new grade.")
        
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
        # Retrieve the grade document to get related student_id and class_id
        grade_data = get_grade_by_id(grade_id)
        if not grade_data:
            print(f"Grade with ID {grade_id} not found.")
            return None

        # Use $pull to remove the grade ID from the student's grades array
        student_update_result = student_collection.update_one(
            {"_id": ObjectId(grade_data['student_id'])},
            {"$pull": {"grades": ObjectId(grade_id)}}
        )

        # Use $pull to remove the grade ID from the class's grades array
        class_update_result = class_collection.update_one(
            {"_id": ObjectId(grade_data['class_id'])},
            {"$pull": {"grades": ObjectId(grade_id)}}
        )

        # Check if the updates were successful
        if student_update_result.modified_count == 0:
            print(f"Failed to update student {grade_data['student_id']} by removing grade {grade_id}.")
        if class_update_result.modified_count == 0:
            print(f"Failed to update class {grade_data['class_id']} by removing grade {grade_id}.")

        # Delete the grade document
        delete_result = grade_collection.delete_one({"_id": ObjectId(grade_id)})
        return {"deleted_count": delete_result.deleted_count}
    except Exception as e:
        print(f"Error deleting grade: {e}")
        return None
    finally:
        client.close()