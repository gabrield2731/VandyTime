import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from app.controllers.student_controller import get_student_by_id, create_student, update_student, delete_student

# Load environment variables for MongoDB connection
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Initialize test database connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vandytime_db"]
student_collection = db["students"]

# Fixture for setting up and tearing down the test database
@pytest.fixture(scope="module")
def test_db():
    # Setup: Clear the test database before starting
    student_collection.delete_many({})
    yield student_collection
    # Teardown: Clear the test database after tests
    student_collection.delete_many({})

# Helper function to create test student data
def create_test_student_data(email, firebase_id):
    return {
        "email": email,
        "firebase_id": firebase_id,
        "classes": [],  # Always empty when inserting a student
        "grades": []    # Always empty when inserting a student
    }

# Test the get_student_by_id function
def test_get_student_by_id(test_db):
    # Create and insert two test students
    student1_data = create_test_student_data(email="student1@test.com", firebase_id="firebase1")
    student2_data = create_test_student_data(email="student2@test.com", firebase_id="firebase2")
    student1_id = test_db.insert_one(student1_data).inserted_id
    student2_id = test_db.insert_one(student2_data).inserted_id

    # Retrieve and validate both students
    fetched_student1 = get_student_by_id(student1_id)
    fetched_student2 = get_student_by_id(student2_id)
    assert fetched_student1 is not None, "Failed to fetch student 1"
    assert fetched_student1["email"] == "student1@test.com"
    assert fetched_student2 is not None, "Failed to fetch student 2"
    assert fetched_student2["email"] == "student2@test.com"

    # Cleanup: Delete test students
    test_db.delete_one({"_id": student1_id})
    test_db.delete_one({"_id": student2_id})

# Test the create_student function
def test_create_student(test_db):
    # Create and insert two test students using the create_student function
    student1_data = create_test_student_data(email="student3@test.com", firebase_id="firebase3")
    student2_data = create_test_student_data(email="student4@test.com", firebase_id="firebase4")

    # Insert students and verify ID is returned
    student1_id = create_student(student1_data)
    assert student1_id is not None, "Failed to insert student 1"

    student2_id = create_student(student2_data)
    assert student2_id is not None, "Failed to insert student 2"

    # Retrieve and validate the students are correctly inserted
    inserted_student1 = test_db.find_one({"_id": ObjectId(student1_id)})
    assert inserted_student1 is not None, "Inserted student 1 was not found in the database"
    assert inserted_student1["email"] == "student3@test.com"

    inserted_student2 = test_db.find_one({"_id": ObjectId(student2_id)})
    assert inserted_student2 is not None, "Inserted student 2 was not found in the database"
    assert inserted_student2["email"] == "student4@test.com"

    # Cleanup: Delete test students
    test_db.delete_one({"_id": ObjectId(student1_id)})
    test_db.delete_one({"_id": ObjectId(student2_id)})

# Test the update_student function
def test_update_student(test_db):
    # Create and insert two test students
    student1_data = create_test_student_data(email="student5@test.com", firebase_id="firebase5")
    student2_data = create_test_student_data(email="student6@test.com", firebase_id="firebase6")
    student1_id = test_db.insert_one(student1_data).inserted_id
    student2_id = test_db.insert_one(student2_data).inserted_id

    # Update the email field for both students
    update_student(student1_id, {"email": "updated_student5@test.com"})
    update_student(student2_id, {"email": "updated_student6@test.com"})

    # Verify that the update was successful
    updated_student1 = test_db.find_one({"_id": student1_id})
    assert updated_student1 is not None, "Failed to update student 1"
    assert updated_student1["email"] == "updated_student5@test.com"

    updated_student2 = test_db.find_one({"_id": student2_id})
    assert updated_student2 is not None, "Failed to update student 2"
    assert updated_student2["email"] == "updated_student6@test.com"

    # Cleanup: Delete test students
    test_db.delete_one({"_id": student1_id})
    test_db.delete_one({"_id": student2_id})

# Test the delete_student function
def test_delete_student(test_db):
    # Create and insert two test students
    student1_data = create_test_student_data(email="student7@test.com", firebase_id="firebase7")
    student2_data = create_test_student_data(email="student8@test.com", firebase_id="firebase8")
    student1_id = test_db.insert_one(student1_data).inserted_id
    student2_id = test_db.insert_one(student2_data).inserted_id

    # Delete the students and verify deletion
    delete_result1 = delete_student(student1_id)
    assert delete_result1["deleted_count"] == 1, "Failed to delete student 1"

    delete_result2 = delete_student(student2_id)
    assert delete_result2["deleted_count"] == 1, "Failed to delete student 2"

    # Verify that both students are no longer in the database
    deleted_student1 = test_db.find_one({"_id": student1_id})
    deleted_student2 = test_db.find_one({"_id": student2_id})

    assert deleted_student1 is None, "Deleted student 1 still found in database"
    assert deleted_student2 is None, "Deleted student 2 still found in database"