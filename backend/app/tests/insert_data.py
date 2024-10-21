from bson import ObjectId  # For ObjectId conversion
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.controllers.class_controller import create_class
from app.controllers.grade_controller import create_grade
from app.controllers.student_controller import create_student

# Helper function to generate ObjectId-like hex values for Firebase IDs
def generate_object_id(firebase_id):
    return ObjectId(firebase_id.zfill(24)[:24])

# Create students with converted Firebase IDs and save their IDs
students = [
    {"email": "gabe@example.com", "firebase_id": generate_object_id("1"), "classes": [], "grades": []},
    {"email": "rohan@example.com", "firebase_id": generate_object_id("2"), "classes": [], "grades": []},
    {"email": "allan@example.com", "firebase_id": generate_object_id("3"), "classes": [], "grades": []},
    {"email": "elena@example.com", "firebase_id": generate_object_id("4"), "classes": [], "grades": []},
]

student_ids = {}  # Store student_id for each student
for student_data in students:
    created_student_id = create_student(student_data)  # Assuming it returns the ObjectId directly
    student_ids[student_data["email"]] = created_student_id  # Save the student ID

# Create classes with descriptions and save their IDs
classes = [
    {"name": "Data Structures", "teacher": "Jerry Roth", "description": "Learn algorithms and data structures.", "grades": []},
    {"name": "Data Structures", "teacher": "Shervin Hajiamini", "description": "Explore advanced data structures.", "grades": []},
    {"name": "Intro to CS", "teacher": "Gina Bai", "description": "Introduction to programming and problem-solving.", "grades": []},
    {"name": "Intro to CS", "teacher": "Md Hasan", "description": "Foundations of computer science and coding.", "grades": []},
    {"name": "Intermediate Software Design", "teacher": "Graham Hemingway", "description": "Design patterns and object-oriented software design.", "grades": []},
    {"name": "Machine Learning", "teacher": "Thomas Beckers", "description": "Introduction to machine learning algorithms.", "grades": []},
    {"name": "Computer Networks", "teacher": "Andy Gokhale", "description": "Study of protocols, architecture, and networking systems.", "grades": []},
    {"name": "Operating Systems", "teacher": "Shervin Hajiamini", "description": "Explore OS principles, memory management, and processes.", "grades": []}
]

class_ids = {}  # Store class_id for each class
for class_data in classes:
    created_class_id = create_class(class_data)  # Assuming it returns the ObjectId directly
    class_ids[(class_data["name"], class_data["teacher"])] = created_class_id  # Save the class ID

# Create grades using the saved student and class IDs
grades = [
    {"student_id": student_ids["gabe@example.com"], "class_id": class_ids[("Data Structures", "Jerry Roth")], "grade": "C"},
    {"student_id": student_ids["gabe@example.com"], "class_id": class_ids[("Intro to CS", "Gina Bai")], "grade": "D"},
    {"student_id": student_ids["gabe@example.com"], "class_id": class_ids[("Intermediate Software Design", "Graham Hemingway")], "grade": "C"},

    {"student_id": student_ids["rohan@example.com"], "class_id": class_ids[("Data Structures", "Jerry Roth")], "grade": "A"},
    {"student_id": student_ids["rohan@example.com"], "class_id": class_ids[("Intro to CS", "Gina Bai")], "grade": "B"},
    {"student_id": student_ids["rohan@example.com"], "class_id": class_ids[("Machine Learning", "Thomas Beckers")], "grade": "A"},

    {"student_id": student_ids["allan@example.com"], "class_id": class_ids[("Intro to CS", "Md Hasan")], "grade": "A"},
    {"student_id": student_ids["allan@example.com"], "class_id": class_ids[("Intermediate Software Design", "Graham Hemingway")], "grade": "B"},

    {"student_id": student_ids["elena@example.com"], "class_id": class_ids[("Data Structures", "Shervin Hajiamini")], "grade": "A"},
    {"student_id": student_ids["elena@example.com"], "class_id": class_ids[("Computer Networks", "Andy Gokhale")], "grade": "A"},
    {"student_id": student_ids["elena@example.com"], "class_id": class_ids[("Operating Systems", "Shervin Hajiamini")], "grade": "B"}
]

# Insert grades using the controller
for grade_data in grades:
    try:
        create_grade(grade_data)
    except Exception as e:
        print(f"Error inserting grade: {e}")

# Print confirmation
print('Data insertion completed.')
