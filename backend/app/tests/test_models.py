from pymongo import MongoClient
import os
from bson.objectid import ObjectId
import pytest
from app.models.class_model import create_class, get_class_by_id, update_class, delete_class
from app.models.grade_model import create_grade, get_grade_by_id, update_grade, delete_grade
from app.models.student_model import create_student, get_student_by_id, update_student, delete_student

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Providing the DB as a global fixture so the tests can access the db
@pytest.fixture(scope="module")
def db():
    client = MongoClient(os.getenv("MONGO_URI"))
    db = client["vandytime_db"]
    yield db
    client.close()

# Test if the collections exist
def test_collections_exist(db):
    collections = db.list_collection_names()
    assert "classes" in collections, "Collection 'classes' does not exist."
    assert "grades" in collections, "Collection 'grades' does not exist."
    assert "students" in collections, "Collection 'students' does not exist."

# Testing class CRUD operations
class TestClassOperations:
    def test_create_class(self, db):
        class_data = {
            "class_name": "Data Structures",
            "class_code": "CS 2201",
            "instructor": "Jerry Roth",
            "credits": 3
        }
        inserted_id = create_class(class_data)
        if inserted_id:
            delete_class(inserted_id)
        assert inserted_id is not None, "Failed to insert class."

    def test_get_class_by_id(self, db):
        class_data = {
            "class_name": "Data Structures",
            "class_code": "CS 2201",
            "instructor": "Jerry Roth",
            "credits": 3
        }
        inserted_id = create_class(class_data)
        class_info = get_class_by_id(inserted_id)
        if inserted_id:
            delete_class(inserted_id)
        assert class_info is not None, "Class not found."

    def test_update_class(self, db):
        class_data = {
            "class_name": "Data Structures",
            "class_code": "CS 2201",
            "instructor": "Jerry Roth",
            "credits": 3
        }
        inserted_id = create_class(class_data)
        update_data = {"instructor": "MD Hasan", "credits": 4}
        update_result = update_class(inserted_id, update_data)
        if inserted_id:
            delete_class(inserted_id)
        assert update_result.matched_count > 0, "No class found with the given ID."

    def test_delete_class(self, db):
        class_data = {
            "class_name": "Data Structures",
            "class_code": "CS 2201",
            "instructor": "Jerry Roth",
            "credits": 3
        }
        inserted_id = create_class(class_data)
        delete_result = delete_class(inserted_id)
        assert delete_result["deleted_count"] > 0, "Failed to delete class."

# Testing grade CRUD operations
class TestGradeOperations:
    def test_create_grade(self, db):
        grade_data = {
            "student_id": "000123456",
            "class_code": "CS 3251",
            "grade": "A-",
            "comments": "Good job"
        }
        inserted_id = create_grade(grade_data)
        if inserted_id:
            delete_grade(inserted_id)
        assert inserted_id is not None, "Failed to insert grade."

    def test_get_grade_by_id(self, db):
        grade_data = {
            "student_id": "000123456",
            "class_code": "CS 3251",
            "grade": "A-",
            "comments": "Good job"
        }
        inserted_id = create_grade(grade_data)
        grade_info = get_grade_by_id(inserted_id)
        if inserted_id:
            delete_grade(inserted_id)
        assert grade_info is not None, "Grade not found."

    def test_update_grade(self, db):
        grade_data = {
            "student_id": "000123456",
            "class_code": "CS 3251",
            "grade": "A-",
            "comments": "Good job"
        }
        inserted_id = create_grade(grade_data)
        update_data = {"grade": "A+", "comments": "Fixed your grade"}
        update_result = update_grade(inserted_id, update_data)
        if inserted_id:
            delete_grade(inserted_id)
        assert update_result.matched_count > 0, "No grade found with the given ID."

    def test_delete_grade(self, db):
        grade_data = {
            "student_id": "000123456",
            "class_code": "CS 3251",
            "grade": "A-",
            "comments": "Good job"
        }
        inserted_id = create_grade(grade_data)
        delete_result = delete_grade(inserted_id)
        assert delete_result["deleted_count"] > 0, "Failed to delete grade."


# Testing student CRUD operations
class TestStudentOperations:
    def test_create_student(self, db):
        student_data = {
            "name": "Nadha Skolar",
            "student_id": "000123456",
            "major": "Computer Science",
            "year": 3
        }
        inserted_id = create_student(student_data)
        if inserted_id:
            delete_student(inserted_id)
        assert inserted_id is not None, "Failed to insert student."

    def test_get_student_by_id(self, db):
        student_data = {
            "name": "Nadha Skolar",
            "student_id": "000123456",
            "major": "Computer Science",
            "year": 3
        }
        inserted_id = create_student(student_data)
        student_info = get_student_by_id(inserted_id)
        if inserted_id:
            delete_student(inserted_id)
        assert student_info is not None, "Student not found."

    def test_update_student(self, db):
        student_data = {
            "name": "Nadha Skolar",
            "student_id": "000123456",
            "major": "Computer Science",
            "year": 3
        }
        inserted_id = create_student(student_data)
        update_data = {"name": "Stellar Skolar", "major": "HOD"}
        update_result = update_student(inserted_id, update_data)
        if inserted_id:
            delete_student(inserted_id)
        assert update_result.matched_count > 0, "No student found with the given ID."

    def test_delete_student(self, db):
        student_data = {
            "name": "Nadha Skolar",
            "student_id": "000123456",
            "major": "Computer Science",
            "year": 3
        }
        inserted_id = create_student(student_data)
        delete_result = delete_student(inserted_id)
        assert delete_result["deleted_count"] > 0, "Failed to delete student."