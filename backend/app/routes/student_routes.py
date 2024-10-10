from flask import Blueprint, request, jsonify
from ..controllers.student_controller import get_student_by_id, create_student, update_student, delete_student

# Create a blueprint for student-related routes
student_bp = Blueprint('student_bp', __name__)

@student_bp.route('/<student_id>', methods=['GET'])
def get_student(student_id):
    student = get_student_by_id(student_id)
    if student:
        return jsonify(student), 200
    return jsonify({"error": "Student not found"}), 404

# Note: can make this different (where it does not pass the grades, and we create an empty grades array for them, connect to auth)
@student_bp.route('/', methods=['POST'])
def add_student():
    """Route to create a new student."""
    student_data = request.json
    result = create_student(student_data)
    # Broken need to implement in create_class function
    return jsonify({"message": "Student created", "id": str(result.inserted_id)}), 201

@student_bp.route('/<student_id>', methods=['PUT'])
def edit_student(student_id):
    """Route to update a student's details."""
    update_data = request.json
    result = update_student(student_id, update_data)
    # Broken need to implement in create_class function
    return jsonify({"message": "Student updated"}), 200 if result.modified_count > 0 else jsonify({"error": "No changes made"}), 400

@student_bp.route('/<student_id>', methods=['DELETE'])
def remove_student(student_id):
    """Route to delete a student."""
    result = delete_student(student_id)
    # Broken need to implement in create_class function
    return jsonify({"message": "Student deleted"}), 200 if result.deleted_count > 0 else jsonify({"error": "Student not found"}), 404
