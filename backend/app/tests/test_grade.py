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

# Fixture for setting up and tearing down the test database
@pytest.fixture(scope="module")
def test_db():
    # Setup: Clear the test database before starting
    grade_collection.delete_many({})
    student_collection.delete_many({})
    class_collection.delete_many({})
    yield grade_collection
    # Teardown: Clear the test database after tests
    grade_collection.delete_many({})
    student_collection.delete_many({})
    class_collection.delete_many({})

# Helper function to create test student data
def create_test_student_data(email, firebase_id):
    return {
        "email": email,
        "firebase_id": firebase_id,
        "classes": [],  # Empty classes list
        "grades": []    # Empty grades list
    }

# Helper function to create test class data
def create_test_class_data(name, semester, teacher):
    return {
        "name": name,
        "semester": semester,
        "teacher": teacher,
        "grades": []  # Empty grades list
    }

# Helper function to create test grade data
def create_test_grade_data(student_id, class_id, grade_value):
    return {
        "student_id": student_id,
        "class_id": class_id,
        "grade": grade_value
    }

# Test the get_grade_by_id function
def test_get_grade_by_id(test_db):
    # Create and insert two test grades
    grade1_data = create_test_grade_data("student1_id", "class1_id", 85)
    grade2_data = create_test_grade_data("student2_id", "class2_id", 90)
    grade1_id = test_db.insert_one(grade1_data).inserted_id
    grade2_id = test_db.insert_one(grade2_data).inserted_id

    # Retrieve and validate both grades
    fetched_grade1 = get_grade_by_id(grade1_id)
    fetched_grade2 = get_grade_by_id(grade2_id)
    assert fetched_grade1 is not None, "Failed to fetch grade 1"
    assert fetched_grade1["grade"] == 85
    assert fetched_grade2 is not None, "Failed to fetch grade 2"
    assert fetched_grade2["grade"] == 90

    # Cleanup: Delete test grades
    test_db.delete_one({"_id": grade1_id})
    test_db.delete_one({"_id": grade2_id})

# Test the create_grade function
def test_create_grade(test_db):
    # Create and insert two dummy students and two dummy classes
    student1_id = create_student(create_test_student_data("student1@test.com", "firebase1"))
    student2_id = create_student(create_test_student_data("student2@test.com", "firebase2"))

    class1_id = create_class(create_test_class_data("Class A", "Fall 2024", "Teacher A"))
    class2_id = create_class(create_test_class_data("Class B", "Spring 2024", "Teacher B"))

    # Create and insert two test grades using the create_grade function
    grade1_data = create_test_grade_data(student1_id, class1_id, 95)
    grade2_data = create_test_grade_data(student2_id, class2_id, 88)

    grade1_id = create_grade(grade1_data)
    assert grade1_id is not None, "Failed to insert grade 1"

    grade2_id = create_grade(grade2_data)
    assert grade2_id is not None, "Failed to insert grade 2"

    # Verify that the grades are correctly inserted in the grade collection
    inserted_grade1 = test_db.find_one({"_id": ObjectId(grade1_id)})
    assert inserted_grade1 is not None, "Inserted grade 1 was not found in the database"
    assert inserted_grade1["grade"] == 95

    inserted_grade2 = test_db.find_one({"_id": ObjectId(grade2_id)})
    assert inserted_grade2 is not None, "Inserted grade 2 was not found in the database"
    assert inserted_grade2["grade"] == 88

    # Cleanup: Delete test grades, students, and classes
    test_db.delete_one({"_id": ObjectId(grade1_id)})
    test_db.delete_one({"_id": ObjectId(grade2_id)})
    student_collection.delete_one({"_id": ObjectId(student1_id)})
    student_collection.delete_one({"_id": ObjectId(student2_id)})
    class_collection.delete_one({"_id": ObjectId(class1_id)})
    class_collection.delete_one({"_id": ObjectId(class2_id)})

# Test the update_grade function
def test_update_grade(test_db):
    # Create and insert a test student and class
    student_id = create_student(create_test_student_data("student3@test.com", "firebase3"))
    class_id = create_class(create_test_class_data("Class C", "Winter 2024", "Teacher C"))

    # Insert a grade
    grade_data = create_test_grade_data(student_id, class_id, 75)
    grade_id = test_db.insert_one(grade_data).inserted_id

    # Update the grade value only
    update_grade(grade_id, {"grade": 80})

    # Verify that the update was successful
    updated_grade = test_db.find_one({"_id": grade_id})
    assert updated_grade is not None, "Failed to update grade"
    assert updated_grade["grade"] == 80

    # Cleanup: Delete test grade, student, and class
    test_db.delete_one({"_id": grade_id})
    student_collection.delete_one({"_id": ObjectId(student_id)})
    class_collection.delete_one({"_id": ObjectId(class_id)})

# Test the delete_grade function
def test_delete_grade(test_db):
    # Create and insert two test grades independently
    grade1_data = create_test_grade_data("dummy_student_id1", "dummy_class_id1", 85)
    grade2_data = create_test_grade_data("dummy_student_id2", "dummy_class_id2", 90)
    grade1_id = test_db.insert_one(grade1_data).inserted_id
    grade2_id = test_db.insert_one(grade2_data).inserted_id

    # Create and insert two dummy students with the grades added
    student1_data = create_test_student_data("student4@test.com", "firebase4")
    student1_data["grades"] = [grade1_id]
    student1_id = student_collection.insert_one(student1_data).inserted_id

    student2_data = create_test_student_data("student5@test.com", "firebase5")
    student2_data["grades"] = [grade2_id]
    student2_id = student_collection.insert_one(student2_data).inserted_id

    # Create and insert two dummy classes with the grades added
    class1_data = create_test_class_data("Class D", "Summer 2024", "Teacher D")
    class1_data["grades"] = [grade1_id]
    class1_id = class_collection.insert_one(class1_data).inserted_id

    class2_data = create_test_class_data("Class E", "Spring 2025", "Teacher E")
    class2_data["grades"] = [grade2_id]
    class2_id = class_collection.insert_one(class2_data).inserted_id

    # Update the grades to have the correct student and class IDs after their creation
    test_db.update_one({"_id": grade1_id}, {"$set": {"student_id": student1_id, "class_id": class1_id}})
    test_db.update_one({"_id": grade2_id}, {"$set": {"student_id": student2_id, "class_id": class2_id}})

    # Delete the grades and verify deletion
    delete_result1 = delete_grade(grade1_id)
    assert delete_result1["deleted_count"] == 1, "Failed to delete grade 1"

    delete_result2 = delete_grade(grade2_id)
    assert delete_result2["deleted_count"] == 1, "Failed to delete grade 2"

    # Verify that the grades are no longer in the database
    deleted_grade1 = test_db.find_one({"_id": grade1_id})
    deleted_grade2 = test_db.find_one({"_id": grade2_id})
    assert deleted_grade1 is None, "Deleted grade 1 still found in database"
    assert deleted_grade2 is None, "Deleted grade 2 still found in database"

    # Verify that the grades have been removed from the student and class documents
    updated_student1 = student_collection.find_one({"_id": ObjectId(student1_id)})
    updated_student2 = student_collection.find_one({"_id": ObjectId(student2_id)})
    updated_class1 = class_collection.find_one({"_id": ObjectId(class1_id)})
    updated_class2 = class_collection.find_one({"_id": ObjectId(class2_id)})

    assert updated_student1 is not None and grade1_id not in updated_student1["grades"], "Grade 1 was not removed from student 1"
    assert updated_student2 is not None and grade2_id not in updated_student2["grades"], "Grade 2 was not removed from student 2"
    assert updated_class1 is not None and grade1_id not in updated_class1["grades"], "Grade 1 was not removed from class 1"
    assert updated_class2 is not None and grade2_id not in updated_class2["grades"], "Grade 2 was not removed from class 2"

    # Cleanup: Delete test students and classes
    student_collection.delete_one({"_id": ObjectId(student1_id)})
    student_collection.delete_one({"_id": ObjectId(student2_id)})
    class_collection.delete_one({"_id": ObjectId(class1_id)})
    class_collection.delete_one({"_id": ObjectId(class2_id)})