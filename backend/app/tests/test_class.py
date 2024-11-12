import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from unittest import mock
from app.controllers.class_controller import get_class_by_id, create_class, update_class, delete_class, get_all_classes, get_teachers_for_class, get_class_by_teacher_and_name, get_all_teachers

# Initialize test database connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vandytime_db"]
class_collection = db["classes"]

# Fixture for setting up and tearing down the test database
@pytest.fixture(scope="module")
def test_db():
    yield class_collection

# Helper function to create test class data using the updated object structure
def create_test_class_data(code, name, description, teacher, grades=[]):
    return {
        "code": code,
        "name": name,
        "description": description,
        "teacher": teacher,
        "grades": grades
    }

# Test the get_class_by_id function
def test_get_class_by_id(test_db):
    class1 = create_test_class_data(
        "CS 4278", "Principles of Software Engineering",
        "The nature of software. The object-oriented paradigm.", "SINGH, V", []
    )
    class1_id = test_db.insert_one(class1).inserted_id

    try:
        fetched_class = get_class_by_id(class1_id)
        assert fetched_class["name"] == "Principles of Software Engineering"
        assert fetched_class["teacher"] == "SINGH, V"
    finally:
        test_db.delete_one({"_id": class1_id})

# Test the create_class function
def test_create_class(test_db):
    class_data = create_test_class_data(
        "CS 1101", "Introduction to CS", 
        "Basic CS concepts.", "SMITH, J", []
    )
    class_id = create_class(class_data)

    try:
        inserted_class = test_db.find_one({"_id": ObjectId(class_id)})
        assert inserted_class["name"] == "Introduction to CS"
        assert inserted_class["teacher"] == "SMITH, J"
    finally:
        test_db.delete_one({"_id": ObjectId(class_id)})

# Test the update_class function
def test_update_class(test_db):
    class_data = create_test_class_data(
        "CS 3250", "Algorithms", 
        "Advanced algorithms course.", "DOE, J", []
    )
    class_id = test_db.insert_one(class_data).inserted_id

    try:
        update_data = {
            "name": "Updated Algorithms",
            "teacher": "DOE, J Updated"
        }
        update_class(class_id, update_data)
        updated_class = test_db.find_one({"_id": class_id})
        assert updated_class["name"] == "Updated Algorithms"
        assert updated_class["teacher"] == "DOE, J Updated"
    finally:
        test_db.delete_one({"_id": class_id})

# Test the delete_class function
def test_delete_class(test_db):
    class_data = create_test_class_data(
        "CS 2201", "Data Structures", 
        "In-depth study of data structures.", "LEE, A", []
    )
    class_id = test_db.insert_one(class_data).inserted_id

    try:
        delete_result = delete_class(class_id)
        assert delete_result["deleted_count"] == 1
        assert test_db.find_one({"_id": class_id}) is None
    finally:
        test_db.delete_one({"_id": class_id})

# Test the get_all_classes function
def test_get_all_classes(test_db):
    class1_id = test_db.insert_one(create_test_class_data(
        "CS 4278", "Principles of Software Engineering", 
        "The nature of software. The object-oriented paradigm.", "SINGH, V", []
    )).inserted_id

    class2_id = test_db.insert_one(create_test_class_data(
        "CS 101", "Introduction to CS", 
        "Basic CS concepts.", "SMITH, J", []
    )).inserted_id

    try:
        all_classes = get_all_classes()
        assert len(all_classes) >= 2, "Expected at least 2 classes in the result"
    finally:
        test_db.delete_one({"_id": class1_id})
        test_db.delete_one({"_id": class2_id})


# Test the get_teachers_for_class function
def test_get_teachers_for_class(test_db):
    class1_id = test_db.insert_one(create_test_class_data(
        "CS 5278", "Grad Principles of Software Engineering", 
        "The nature of software. The object-oriented paradigm.", "SINGH, V", []
    )).inserted_id

    try:
        teachers = get_teachers_for_class("Grad Principles of Software Engineering")
        assert len(teachers) == 1, "Expected 1 teacher"
        assert "SINGH, V" in teachers, "Expected 'SINGH, V' in teacher list"
    finally:
        test_db.delete_one({"_id": class1_id})


# Test the get_class_by_teacher_and_name function
def test_get_class_by_teacher_and_name(test_db):
    class_id = test_db.insert_one(create_test_class_data(
        "CS 4278", "Principles of Software Engineering", 
        "The nature of software. The object-oriented paradigm.", "SINGH, V", []
    )).inserted_id

    try:
        class_obj = get_class_by_teacher_and_name("Principles of Software Engineering", "SINGH, V")
        assert class_obj is not None, "Class not found"
        assert class_obj["name"] == "Principles of Software Engineering"
        assert class_obj["teacher"] == "SINGH, V"
    finally:
        test_db.delete_one({"_id": class_id})


# Test the get_all_teachers function
def test_get_all_teachers(test_db):
    class1_id = test_db.insert_one(create_test_class_data(
        "CS 4278", "Principles of Software Engineering", 
        "The nature of software. The object-oriented paradigm.", "SINGH, V", []
    )).inserted_id

    class2_id = test_db.insert_one(create_test_class_data(
        "CS 101", "Introduction to CS", 
        "Basic CS concepts.", "SMITH, J", []
    )).inserted_id

    try:
        teachers = get_all_teachers()
        assert "SINGH, V" in teachers, "Expected 'SINGH, V' in teacher list"
        assert "SMITH, J" in teachers, "Expected 'SMITH, J' in teacher list"
    finally:
        test_db.delete_one({"_id": class1_id})
        test_db.delete_one({"_id": class2_id})

# Exception tests

# Test for exception in get_class_by_id
@mock.patch("app.controllers.class_controller.MongoClient")
def test_get_class_by_id_exception(MockMongoClient):
    # Simulate an exception in find_one
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].find_one.side_effect = Exception("Database error")

    result = get_class_by_id("someid")
    assert result is None, "Expected None due to exception in get_class_by_id"

# Test for exception in create_class
@mock.patch("app.controllers.class_controller.MongoClient")
def test_create_class_exception(MockMongoClient):
    # Simulate an exception in insert_one
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].insert_one.side_effect = Exception("Insert error")

    class_data = {
        "name": "Exception Class", 
        "teacher": "SMITH, J", 
        "grades": []
    }
    result = create_class(class_data)
    assert result is None, "Expected None due to exception in create_class"

# Test for exception in update_class
@mock.patch("app.controllers.class_controller.MongoClient")
def test_update_class_exception(MockMongoClient):
    # Simulate an exception in update_one
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].update_one.side_effect = Exception("Update error")

    update_data = {"name": "Updated Name"}
    result = update_class("someid", update_data)
    assert result is None, "Expected None due to exception in update_class"

# Test for exception in delete_class
@mock.patch("app.controllers.class_controller.MongoClient")
def test_delete_class_exception(MockMongoClient):
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].delete_one.side_effect = Exception("Delete error")

    result = delete_class("someid")
    assert "deleted_count" in result, "Expected error key in delete_class result due to exception"
    assert result["deleted_count"] == 0, "Expected specific error message in delete_class result"

# Test for exception in get_all_classes
@mock.patch("app.controllers.class_controller.MongoClient")
def test_get_all_classes_exception(MockMongoClient):
    # Simulate an exception in find
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].find.side_effect = Exception("Find error")

    result = get_all_classes()
    assert result is None, "Expected None due to exception in get_all_classes"

# Test for exception in get_teachers_for_class
@mock.patch("app.controllers.class_controller.get_all_classes")
def test_get_teachers_for_class_exception(MockGetAllClasses):
    # Simulate an exception in get_all_classes
    MockGetAllClasses.side_effect = Exception("Get all classes error")

    result = get_teachers_for_class("Some Class")
    assert result is None, "Expected None due to exception in get_teachers_for_class"

# Test for exception in get_class_by_teacher_and_name
@mock.patch("app.controllers.class_controller.MongoClient")
def test_get_class_by_teacher_and_name_exception(MockMongoClient):
    # Simulate an exception in find_one with regex
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].find_one.side_effect = Exception("Find error with regex")

    result = get_class_by_teacher_and_name("Some Name", "Some Teacher")
    assert result is None, "Expected None due to exception in get_class_by_teacher_and_name"

# Test for exception in get_all_teachers
@mock.patch("app.controllers.class_controller.MongoClient")
def test_get_all_teachers_exception(MockMongoClient):
    # Simulate an exception in distinct
    mock_client = MockMongoClient.return_value
    mock_client["vandytime_db"]["classes"].distinct.side_effect = Exception("Distinct error")

    result = get_all_teachers()
    assert result is None, "Expected None due to exception in get_all_teachers"
