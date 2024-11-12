import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from unittest import mock
from app.controllers.student_controller import get_student_by_id, create_student, update_student, delete_student, get_student_by_fid

# Load environment variables for MongoDB connection
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Initialize test database connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vandytime_db"]
student_collection = db["students"]

@pytest.fixture(scope="module")
def test_db():
    yield student_collection

# Helper function to create test student data
def create_test_student_data(email, firebase_id):
    return {
        "email": email,
        "firebase_id": firebase_id,
        "classes": [],
        "grades": []
    }

# Test the get_student_by_id function
def test_get_student_by_id(test_db):
    student1 = create_test_student_data("student1@test.com", "firebase1")
    student2 = create_test_student_data("student2@test.com", "firebase2")

    student1_id = test_db.insert_one(student1).inserted_id
    student2_id = test_db.insert_one(student2).inserted_id

    try:
        fetched_student1 = get_student_by_id(student1_id)
        fetched_student2 = get_student_by_id(student2_id)

        assert fetched_student1["email"] == "student1@test.com"
        assert fetched_student2["email"] == "student2@test.com"
    finally:
        test_db.delete_one({"_id": student1_id})
        test_db.delete_one({"_id": student2_id})

# Test the create_student function
def test_create_student(test_db):
    student1 = create_test_student_data("student3@test.com", "firebase3")
    student2 = create_test_student_data("student4@test.com", "firebase4")

    student1_id = create_student(student1).inserted_id
    student2_id = create_student(student2).inserted_id

    try:
        inserted_student1 = test_db.find_one({"_id": ObjectId(student1_id)})
        inserted_student2 = test_db.find_one({"_id": ObjectId(student2_id)})

        assert inserted_student1["email"] == "student3@test.com"
        assert inserted_student2["email"] == "student4@test.com"
    finally:
        test_db.delete_one({"_id": ObjectId(student1_id)})
        test_db.delete_one({"_id": ObjectId(student2_id)})

# Test the update_student function
def test_update_student(test_db):
    student1 = create_test_student_data("student5@test.com", "firebase5")
    student2 = create_test_student_data("student6@test.com", "firebase6")

    student1_id = test_db.insert_one(student1).inserted_id
    student2_id = test_db.insert_one(student2).inserted_id

    try:
        update_student(student1_id, {"email": "updated_student5@test.com"})
        update_student(student2_id, {"email": "updated_student6@test.com"})

        updated_student1 = test_db.find_one({"_id": student1_id})
        updated_student2 = test_db.find_one({"_id": student2_id})

        assert updated_student1["email"] == "updated_student5@test.com"
        assert updated_student2["email"] == "updated_student6@test.com"
    finally:
        test_db.delete_one({"_id": student1_id})
        test_db.delete_one({"_id": student2_id})

# Test the delete_student function
def test_delete_student(test_db):
    student1 = create_test_student_data("student7@test.com", "firebase7")
    student2 = create_test_student_data("student8@test.com", "firebase8")

    student1_id = test_db.insert_one(student1).inserted_id
    student2_id = test_db.insert_one(student2).inserted_id

    try:
        assert delete_student(student1_id)["deleted_count"] == 1
        assert delete_student(student2_id)["deleted_count"] == 1

        assert test_db.find_one({"_id": student1_id}) is None
        assert test_db.find_one({"_id": student2_id}) is None
    finally:
        # Ensure cleanup even if tests fail
        test_db.delete_one({"_id": student1_id})
        test_db.delete_one({"_id": student2_id})

# Test for exception handling in get_student_by_id
@mock.patch("app.controllers.student_controller.MongoClient")
def test_get_student_by_id_exception(MockMongoClient):
    # Mock the MongoDB client to raise an exception on find_one
    mock_client = MockMongoClient.return_value
    mock_db = mock_client["vandytime_db"]
    mock_db["students"].find_one.side_effect = Exception("Database error")

    # Call get_student_by_id and check the result
    result = get_student_by_id("someid")
    assert result is None, "Expected None due to exception in get_student_by_id"

# Test for exception handling in get_student_by_fid
@mock.patch("app.controllers.student_controller.MongoClient")
def test_get_student_by_fid_exception(MockMongoClient):
    # Mock the MongoDB client to raise an exception on find_one
    mock_client = MockMongoClient.return_value
    mock_db = mock_client["vandytime_db"]
    mock_db["students"].find_one.side_effect = Exception("Database error")

    # Call get_student_by_fid and check the result
    result = get_student_by_fid("firebase_id")
    assert result is None, "Expected None due to exception in get_student_by_fid"

# Test for exception handling in create_student
@mock.patch("app.controllers.student_controller.MongoClient")
def test_create_student_exception(MockMongoClient):
    # Mock the MongoDB client to raise an exception on insert_one
    mock_client = MockMongoClient.return_value
    mock_db = mock_client["vandytime_db"]
    mock_db["students"].insert_one.side_effect = Exception("Insert error")

    student_data = {
        "name": "Test Student",
        "grades": []
    }
    
    # Call create_student and check the result
    result = create_student(student_data)
    assert result is None, "Expected None due to exception in create_student"

# Test for exception handling in update_student
@mock.patch("app.controllers.student_controller.MongoClient")
def test_update_student_exception(MockMongoClient):
    # Mock the MongoDB client to raise an exception on update_one
    mock_client = MockMongoClient.return_value
    mock_db = mock_client["vandytime_db"]
    mock_db["students"].update_one.side_effect = Exception("Update error")

    update_data = {"name": "Updated Name"}
    
    # Call update_student and check the result
    result = update_student("someid", update_data)
    assert result is None, "Expected None due to exception in update_student"

# Test for exception handling in delete_student
@mock.patch("app.controllers.student_controller.MongoClient")
@mock.patch("app.controllers.student_controller.get_student_by_id")
@mock.patch("app.controllers.grade_controller.delete_grade", return_value=None)  # Mock delete_grade to do nothing
def test_delete_student_exception(mock_delete_grade, mock_get_student_by_id, MockMongoClient):
    # Set up get_student_by_id to return a student with grades so delete operations are attempted
    mock_get_student_by_id.return_value = {
        "_id": "someid",
        "grades": ["grade1", "grade2"]
    }

    # Mock the MongoDB client to raise an exception on delete_one
    mock_client = MockMongoClient.return_value
    mock_db = mock_client["vandytime_db"]
    mock_db["students"].delete_one.side_effect = Exception("Delete error")

    # Call delete_student and check the result
    result = delete_student("someid")
    assert "error" in result, "Expected 'error' key in result due to exception in delete_one"
