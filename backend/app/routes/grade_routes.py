from flask import Blueprint, request, jsonify
from ..controllers.grade_controller import get_grade_by_id, create_grade, update_grade, delete_grade, get_grades_by_class
from bson.objectid import ObjectId

grade_bp = Blueprint('grade_bp', __name__)

def process_data(data):
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, list):
            data[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return data

@grade_bp.route('/<grade_id>', methods=['GET'])
def get_grade(grade_id):
    """Route to fetch a grade by ID"""
    grade = get_grade_by_id(grade_id)
    if grade:
        return jsonify(process_data(grade)), 200
    return jsonify({"error": "Grade not found"}), 404

@grade_bp.route('/', methods=['POST'])
def add_grade():
    """Route to create a new grade."""
    grade_data = request.json
    result = create_grade(grade_data)
    return jsonify({"message": "Grade created", "id": str(result)}), 201

@grade_bp.route('/<grade_id>', methods=['PUT'])
def edit_grade(grade_id):
    """Route to update a grade's details."""
    update_data = request.json
    result = update_grade(grade_id, update_data)
    # Broken need to implement in create_class function
    if result and result.modified_count > 0:
        return jsonify({"message": "Grade updated"}), 200
    else:
        return jsonify({"error": "No changes made"}), 400

@grade_bp.route('/<grade_id>', methods=['DELETE'])
def remove_grade(grade_id):
    """Route to delete a grade."""
    result = delete_grade(grade_id)
    if result and result["deleted_count"] > 0:
        return jsonify({"message": "Grade deleted"}), 200
    else:
        return jsonify({"error": "Grade not found"}), 404

@grade_bp.route('/<class_id>/<year>/<semester>', methods=['GET'])
def get_grades_by_sem(class_id, year, semester):
    """Route to fetch all grades for a class in a specific year and semester"""
    result = get_grades_by_class(class_id, year, semester)

    if result or result == []:
        return jsonify(result), 200
    return jsonify({"error": "Grades not found"}), 404
