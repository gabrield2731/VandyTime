import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from app.controllers.class_controller import get_class_by_id, create_class, update_class, delete_class

# Initialize test database connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vandytime_db"]
class_collection = db["classes"]

# Fixture for setting up and tearing down the test database
@pytest.fixture(scope="module")
def test_db():
    # Setup: Clear the test database before starting
    class_collection.delete_many({})
    yield class_collection
    # Teardown: Clear the test database after tests
    class_collection.delete_many({})

# Helper function to create test class data without default values
def create_test_class_data(name, semester, teacher, grades):
    return {
        "name": name,
        "semester": semester,
        "teacher": teacher,
        "grades": grades
    }

# Test the get_class_by_id function
def test_get_class_by_id(test_db):
    # Insert test classes
    class1 = create_test_class_data(name="Class A", semester="Fall 2024", teacher="Teacher A", grades=[])
    class2 = create_test_class_data(name="Class B", semester="Spring 2024", teacher="Teacher B", grades=[])
    class1_id = test_db.insert_one(class1).inserted_id
    class2_id = test_db.insert_one(class2).inserted_id

    # Test getting each class by ID
    fetched_class1 = get_class_by_id(class1_id)
    fetched_class2 = get_class_by_id(class2_id)
    assert fetched_class1["name"] == "Class A"
    assert fetched_class2["name"] == "Class B"

    # Cleanup: Delete test classes
    test_db.delete_one({"_id": class1_id})
    test_db.delete_one({"_id": class2_id})

# Test the create_class function
def test_create_class(test_db):
    # Create and insert test classes
    class1_data = create_test_class_data(name="Class C", semester="Fall 2024", teacher="Teacher C", grades=[])
    class2_data = create_test_class_data(name="Class D", semester="Spring 2024", teacher="Teacher D", grades=[])
    class1_id = create_class(class1_data)
    class2_id = create_class(class2_data)

    # Verify the classes are inserted and can be retrieved
    inserted_class1 = test_db.find_one({"_id": ObjectId(class1_id)})
    inserted_class2 = test_db.find_one({"_id": ObjectId(class2_id)})
    assert inserted_class1["name"] == "Class C"
    assert inserted_class2["name"] == "Class D"

    # Cleanup: Delete test classes
    test_db.delete_one({"_id": ObjectId(class1_id)})
    test_db.delete_one({"_id": ObjectId(class2_id)})

# Test the update_class function
def test_update_class(test_db):
    # Insert a test class
    class_data = create_test_class_data(name="Class E", semester="Spring 2024", teacher="Teacher E", grades=[])
    class_id = test_db.insert_one(class_data).inserted_id

    # Update the class name, semester, and teacher fields
    update_data = {
        "name": "Updated Class E",
        "semester": "Fall 2024",
        "teacher": "Updated Teacher E"
    }
    update_class(class_id, update_data)

    # Verify that the update was successful
    updated_class = test_db.find_one({"_id": class_id})
    assert updated_class["name"] == "Updated Class E"
    assert updated_class["semester"] == "Fall 2024"
    assert updated_class["teacher"] == "Updated Teacher E"

    # Cleanup: Delete the test class
    test_db.delete_one({"_id": class_id})

# Test the delete_class function
def test_delete_class(test_db):
    # Insert a test class
    class_data = create_test_class_data(name="Class F", semester="Summer 2024", teacher="Teacher F", grades=[])
    class_id = test_db.insert_one(class_data).inserted_id

    # Delete the class and verify deletion
    delete_result = delete_class(class_id)
    assert delete_result["deleted_count"] == 1

    # Verify that the class is no longer in the database
    deleted_class = test_db.find_one({"_id": class_id})
    assert deleted_class is None
