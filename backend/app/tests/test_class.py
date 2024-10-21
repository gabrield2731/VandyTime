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
    # No setup or teardown that clears everything, just return the collection
    yield class_collection

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
    # Insert test classes and store IDs
    class1 = create_test_class_data("Class A", "Fall 2024", "Teacher A", [])
    class2 = create_test_class_data("Class B", "Spring 2024", "Teacher B", [])
    class1_id = test_db.insert_one(class1).inserted_id
    class2_id = test_db.insert_one(class2).inserted_id

    try:
        # Test getting each class by ID
        fetched_class1 = get_class_by_id(class1_id)
        fetched_class2 = get_class_by_id(class2_id)
        assert fetched_class1["name"] == "Class A"
        assert fetched_class2["name"] == "Class B"
    finally:
        # Cleanup: Delete only the inserted classes
        test_db.delete_one({"_id": class1_id})
        test_db.delete_one({"_id": class2_id})

# Test the create_class function
def test_create_class(test_db):
    # Create and insert test classes
    class1_data = create_test_class_data("Class C", "Fall 2024", "Teacher C", [])
    class2_data = create_test_class_data("Class D", "Spring 2024", "Teacher D", [])
    class1_id = create_class(class1_data)
    class2_id = create_class(class2_data)

    try:
        # Verify the classes are inserted and can be retrieved
        inserted_class1 = test_db.find_one({"_id": ObjectId(class1_id)})
        inserted_class2 = test_db.find_one({"_id": ObjectId(class2_id)})
        assert inserted_class1["name"] == "Class C"
        assert inserted_class2["name"] == "Class D"
    finally:
        # Cleanup: Delete the inserted classes
        test_db.delete_one({"_id": ObjectId(class1_id)})
        test_db.delete_one({"_id": ObjectId(class2_id)})

# Test the update_class function
def test_update_class(test_db):
    # Insert a test class
    class_data = create_test_class_data("Class E", "Spring 2024", "Teacher E", [])
    class_id = test_db.insert_one(class_data).inserted_id

    try:
        # Update the class fields
        update_data = {
            "name": "Updated Class E",
            "semester": "Fall 2024",
            "teacher": "Updated Teacher E"
        }
        update_class(class_id, update_data)

        # Verify the update was successful
        updated_class = test_db.find_one({"_id": class_id})
        assert updated_class["name"] == "Updated Class E"
        assert updated_class["semester"] == "Fall 2024"
        assert updated_class["teacher"] == "Updated Teacher E"
    finally:
        # Cleanup: Delete the inserted class
        test_db.delete_one({"_id": class_id})

# Test the delete_class function
def test_delete_class(test_db):
    # Insert a test class
    class_data = create_test_class_data("Class F", "Summer 2024", "Teacher F", [])
    class_id = test_db.insert_one(class_data).inserted_id

    # Delete the class and verify deletion
    delete_result = delete_class(class_id)
    assert delete_result["deleted_count"] == 1

    # Verify the class no longer exists
    deleted_class = test_db.find_one({"_id": class_id})
    assert deleted_class is None
