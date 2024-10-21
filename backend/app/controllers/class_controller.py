from pymongo import MongoClient
from bson.objectid import ObjectId
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
        if "grades" not in class_data:
            class_data["grades"] = []

        if "teacher" not in class_data:
            return None
        
        if "name" not in class_data:
            return None
        
        if get_class_by_teacher_and_name(class_data["name"], class_data["teacher"]):
            return None

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
        print(update_data)
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
        # Fetch the class data
        class_data = get_class_by_id(class_id)
        
        if not class_data:
            return {"deleted_count": 0}

        class_grades = class_data.get("grades", [])
        for grade_id in class_grades:
            delete_grade(grade_id)

        delete_object = class_collection.delete_one({"_id": ObjectId(class_id)})

        return {"deleted_count": delete_object.deleted_count}
    except Exception as e:
        print(f"Error deleting class: {e}")
        return {"error": str(e)}
    finally:
        client.close()

# Get all classes from the MongoDB collection
def get_all_classes():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    class_collection = db["classes"]

    try:
        class_list = list(class_collection.find())
        for class_data in class_list:
            class_data["_id"] = str(class_data["_id"])
        return class_list
    except Exception as e:
        print(f"Error getting all classes: {e}")
        return None
    finally:
        client.close()

# Get all teachers for a class
def get_teachers_for_class(class_name):
    try:
        classes = get_all_classes()
        teacher_list = []
        for class_data in classes:
            if class_data["name"].lower() == class_name.lower():
                teacher_list.append(class_data["teacher"])
        return teacher_list
    except Exception as e:
        print(f"Error getting teachers for class: {e}")
        return None


# Get class from teacher and name
def get_class_by_teacher_and_name(name, teacher):
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    class_collection = db["classes"]

    try:
        class_object = class_collection.find_one({"teacher": teacher, "name": name})
        return class_object
    except Exception as e:
        print(f"Error getting class by teacher and name: {e}")
        return None
    finally:
        client.close()
