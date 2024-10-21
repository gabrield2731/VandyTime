import pytest
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from app.controllers.grade_controller import get_grade_by_id, create_grade, update_grade, delete_grade
from app.controllers.student_controller import create_student
from app.controllers.class_controller import create_class

# Load environment variables for MongoDB connection
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Initialize test database connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vandytime_db"]
grade_collection = db["grades"]
student_collection = db["students"]
class_collection = db["classes"]

@pytest.fixture(scope="module")
def test_db():
    yield grade_collection  # Return the collection to use in the tests

def create_test_student_data(email, firebase_id):
    return {
        "email": email,
        "firebase_id": firebase_id,
        "classes": [],
        "grades": []
    }

def create_test_class_data(name, semester, teacher):
    return {
        "name": name,
        "semester": semester,
        "teacher": teacher,
        "grades": []
    }

def create_test_grade_data(student_id, class_id, grade_value):
    return {
        "student_id": student_id,
        "class_id": class_id,
        "grade": grade_value
    }

def test_get_grade_by_id(test_db):
    grade1 = create_test_grade_data("student1_id", "class1_id", 85)
    grade2 = create_test_grade_data("student2_id", "class2_id", 90)

    grade1_id = test_db.insert_one(grade1).inserted_id
    grade2_id = test_db.insert_one(grade2).inserted_id

    try:
        fetched_grade1 = get_grade_by_id(grade1_id)
        fetched_grade2 = get_grade_by_id(grade2_id)
        assert fetched_grade1["grade"] == 85
        assert fetched_grade2["grade"] == 90
    finally:
        test_db.delete_one({"_id": grade1_id})
        test_db.delete_one({"_id": grade2_id})

def test_create_grade(test_db):
    student1_id = create_student(create_test_student_data("student1@test.com", "firebase1"))
    student2_id = create_student(create_test_student_data("student2@test.com", "firebase2"))

    class1_id = create_class(create_test_class_data("Class A", "Fall 2024", "Teacher A"))
    class2_id = create_class(create_test_class_data("Class B", "Spring 2024", "Teacher B"))

    grade1 = create_test_grade_data(student1_id, class1_id, 95)
    grade2 = create_test_grade_data(student2_id, class2_id, 88)

    grade1_id = create_grade(grade1)
    grade2_id = create_grade(grade2)

    try:
        assert test_db.find_one({"_id": ObjectId(grade1_id)})["grade"] == 95
        assert test_db.find_one({"_id": ObjectId(grade2_id)})["grade"] == 88
    finally:
        test_db.delete_one({"_id": ObjectId(grade1_id)})
        test_db.delete_one({"_id": ObjectId(grade2_id)})
        student_collection.delete_one({"_id": ObjectId(student1_id)})
        student_collection.delete_one({"_id": ObjectId(student2_id)})
        class_collection.delete_one({"_id": ObjectId(class1_id)})
        class_collection.delete_one({"_id": ObjectId(class2_id)})

def test_update_grade(test_db):
    student_id = create_student(create_test_student_data("student3@test.com", "firebase3"))
    class_id = create_class(create_test_class_data("Class C", "Winter 2024", "Teacher C"))

    grade = create_test_grade_data(student_id, class_id, 75)
    grade_id = test_db.insert_one(grade).inserted_id

    try:
        update_grade(grade_id, {"grade": 80})
        assert test_db.find_one({"_id": grade_id})["grade"] == 80
    finally:
        test_db.delete_one({"_id": grade_id})
        student_collection.delete_one({"_id": ObjectId(student_id)})
        class_collection.delete_one({"_id": ObjectId(class_id)})

def test_delete_grade(test_db):
    student1 = create_test_student_data("student4@test.com", "firebase4")
    student2 = create_test_student_data("student5@test.com", "firebase5")

    student1_id = student_collection.insert_one(student1).inserted_id
    student2_id = student_collection.insert_one(student2).inserted_id

    class1 = create_test_class_data("Class D", "Summer 2024", "Teacher D")
    class2 = create_test_class_data("Class E", "Spring 2025", "Teacher E")

    class1_id = class_collection.insert_one(class1).inserted_id
    class2_id = class_collection.insert_one(class2).inserted_id

    grade1 = create_test_grade_data(student1_id, class1_id, 85)
    grade2 = create_test_grade_data(student2_id, class2_id, 90)

    grade1_id = test_db.insert_one(grade1).inserted_id
    grade2_id = test_db.insert_one(grade2).inserted_id

    try:
        assert delete_grade(grade1_id)["deleted_count"] == 1
        assert delete_grade(grade2_id)["deleted_count"] == 1

        assert test_db.find_one({"_id": grade1_id}) is None
        assert test_db.find_one({"_id": grade2_id}) is None
    finally:
        student_collection.delete_one({"_id": ObjectId(student1_id)})
        student_collection.delete_one({"_id": ObjectId(student2_id)})
        class_collection.delete_one({"_id": ObjectId(class1_id)})
        class_collection.delete_one({"_id": ObjectId(class2_id)})
