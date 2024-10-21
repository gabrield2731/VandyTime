from flask import Blueprint, request, jsonify
from ..controllers.student_controller import get_student_by_id, create_student, update_student, delete_student
from bson.objectid import ObjectId

# Create a blueprint for student-related route
student_bp = Blueprint('student_bp', __name__)

def process_data(data):
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, list):
            data[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return data

@student_bp.route('/<student_id>', methods=['GET'])
def get_student(student_id):
    student = get_student_by_id(student_id)
    if student:
        return jsonify(process_data(student)), 200
    return jsonify({"error": "Student not found"}), 404

@student_bp.route('/', methods=['POST'])
def add_student():
    """Route to create a new student."""
    student_data = request.json
    result = create_student(student_data)
    return jsonify({"message": "Student created", "id": str(result.inserted_id)}), 201

@student_bp.route('/<student_id>', methods=['PUT'])
def edit_student(student_id):
    """Route to update a student's details."""
    update_data = request.json
    result = update_student(student_id, update_data)
    if result and result.modified_count > 0:
        return jsonify({"message": "Student updated"}), 200
    else:
        return jsonify({"error": "No changes made"}), 400

@student_bp.route('/<student_id>', methods=['DELETE'])
def remove_student(student_id):
    """Route to delete a student."""
    result = delete_student(student_id)
    if result and result["deleted_count"] > 0:
        return jsonify({"message": "Student deleted"}), 200
    else:
        return jsonify({"error": "Student not found"}), 404
