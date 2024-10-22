import pytest
from bson.objectid import ObjectId
from app.controllers.grade_controller import create_grade, get_grade_by_id, update_grade, delete_grade
from app.controllers.student_controller import create_student
from app.controllers.class_controller import create_class
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient

# Load environment variables for MongoDB connection
load_dotenv(find_dotenv())

# Initialize MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["vandytime_db"]
grade_collection = db["grades"]
student_collection = db["students"]
class_collection = db["classes"]

@pytest.fixture(scope="module")
def test_db():
    yield grade_collection

def create_test_student_data(email, firebase_id):
    return {"email": email, "firebase_id": firebase_id, "classes": [], "grades": []}

def create_test_class_data(name, semester, teacher):
    return {"name": name, "semester": semester, "teacher": teacher, "grades": []}

def create_test_grade_data(student_id, class_id, grade_value):
    return {"student_id": student_id, "class_id": class_id, "grade": grade_value}

# Test the get_grade_by_id function
def test_get_grade_by_id(test_db):
    grade1 = create_test_grade_data("student1_id", "class1_id", 85)
    grade2 = create_test_grade_data("student2_id", "class2_id", 90)

    grade1_id = test_db.insert_one(grade1).inserted_id
    grade2_id = test_db.insert_one(grade2).inserted_id

    try:
        assert get_grade_by_id(grade1_id)["grade"] == 85, f"Expected 85 but got {get_grade_by_id(grade1_id)}"
        assert get_grade_by_id(grade2_id)["grade"] == 90, f"Expected 90 but got {get_grade_by_id(grade2_id)}"
    finally:
        test_db.delete_one({"_id": grade1_id})
        test_db.delete_one({"_id": grade2_id})

# Test the create_grade function
# Test the create_grade function
def test_create_grade(test_db):
    # Create students and classes first
    student1 = create_test_student_data("student1@test.com", "firebase1")
    student2 = create_test_student_data("student2@test.com", "firebase2")

    student1_id = create_student(student1).inserted_id
    student2_id = create_student(student2).inserted_id

    class1 = create_test_class_data("Class A", "Fall 2024", "Teacher A")
    class2 = create_test_class_data("Class B", "Spring 2024", "Teacher B")

    class1_id = create_class(class1)
    class2_id = create_class(class2)

    grade1_id = create_grade(create_test_grade_data(student1_id, class1_id, 95))
    grade2_id = create_grade(create_test_grade_data(student2_id, class2_id, 88))

    try:
        grade1 = test_db.find_one({"_id": ObjectId(grade1_id)})
        grade2 = test_db.find_one({"_id": ObjectId(grade2_id)})

        assert grade1 is not None, "Grade 1 not found in the database"
        assert grade2 is not None, "Grade 2 not found in the database"
        assert grade1["grade"] == 95, f"Expected grade 95, but got {grade1['grade']}"
        assert grade2["grade"] == 88, f"Expected grade 88, but got {grade2['grade']}"

    finally:
        test_db.delete_one({"_id": ObjectId(grade1_id)}) if grade1_id else None
        test_db.delete_one({"_id": ObjectId(grade2_id)}) if grade2_id else None
        student_collection.delete_one({"_id": ObjectId(student1_id)})
        student_collection.delete_one({"_id": ObjectId(student2_id)})
        class_collection.delete_one({"_id": ObjectId(class1_id)})
        class_collection.delete_one({"_id": ObjectId(class2_id)})

# Test the update_grade function
def test_update_grade(test_db):
    student = create_test_student_data("student3@test.com", "firebase3")
    student_id = create_student(student).inserted_id

    class_ = create_test_class_data("Class C", "Winter 2024", "Teacher C")
    class_id = create_class(class_)

    grade_id = create_grade(create_test_grade_data(student_id, class_id, 75))

    try:
        update_result = update_grade(grade_id, {"grade": 80})
        assert update_result.modified_count == 1, "Failed to update grade"

        updated_grade = test_db.find_one({"_id": ObjectId(grade_id)})
        assert updated_grade["grade"] == 80, f"Expected 80 but got {updated_grade['grade']}"

    finally:
        test_db.delete_one({"_id": ObjectId(grade_id)})
        student_collection.delete_one({"_id": ObjectId(student_id)})
        class_collection.delete_one({"_id": ObjectId(class_id)})

# Test the delete_grade function
def test_delete_grade(test_db):
    student1_id = student_collection.insert_one(create_test_student_data("student4@test.com", "firebase4")).inserted_id
    class1_id = class_collection.insert_one(create_test_class_data("Class D", "Summer 2024", "Teacher D")).inserted_id

    grade_id = create_grade(create_test_grade_data(student1_id, class1_id, 85))

    try:
        delete_result = delete_grade(grade_id)
        assert delete_result["deleted_count"] == 1, "Failed to delete grade"
        assert test_db.find_one({"_id": ObjectId(grade_id)}) is None, "Grade not deleted"
    finally:
        student_collection.delete_one({"_id": ObjectId(student1_id)})
        class_collection.delete_one({"_id": ObjectId(class1_id)})
