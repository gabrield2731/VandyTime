from flask import Blueprint, request, jsonify
from ..controllers.class_controller import get_class_by_id, create_class, update_class, delete_class, get_all_classes, get_teachers_for_class, get_class_by_teacher_and_name, get_all_teachers
from bson.objectid import ObjectId

class_bp = Blueprint('class_bp', __name__)

def process_data(data):
    for key, value in data.items():
        if isinstance(value, ObjectId):
            data[key] = str(value)
        elif isinstance(value, list):
            data[key] = [str(v) if isinstance(v, ObjectId) else v for v in value]
    return data

@class_bp.route('/<class_id>', methods=['GET'])
def get_class(class_id):
    """Route to fetch a class by ID"""
    class_info = get_class_by_id(class_id)
    if class_info:
        return jsonify(process_data(class_info)), 200
    return jsonify({"error": "Class not found"}), 404

@class_bp.route('/', methods=['POST'])
def add_class():
    """Route to create a new class"""
    class_data = request.json
    result = create_class(class_data)
    
    if result:
        return jsonify({"message": "Class created", "id": str(result)}), 201
    else:
        return jsonify({"error": "Error creating class"}), 400

@class_bp.route('/<class_id>', methods=['PUT'])
def edit_class(class_id):
    """Route to update a class's details."""
    update_data = request.json
    result = update_class(class_id, update_data)
    
    if result and result.modified_count > 0:
        return jsonify({"message": "Class updated"}), 200
    else:
        return jsonify({"error": "No changes made"}), 400

@class_bp.route('/<class_id>', methods=['DELETE'])
def remove_class(class_id):
    """Route to delete a class."""
    result = delete_class(class_id)

    if result and result["deleted_count"] > 0:
        return jsonify({"message": "Class deleted"}), 200
    else:
        return jsonify({"error": "Class not found"}), 404

@class_bp.route('/', methods=['GET'])
def get_classes():
    """Route to fetch all classes"""
    return jsonify(get_all_classes()), 200

@class_bp.route('/<class_name>/teachers', methods=['GET'])
def get_teachers(class_name):
    """Route to fetch all teachers for a class"""
    teachers = get_teachers_for_class(class_name)
    if teachers:
        return jsonify(teachers), 200
    else:
        return jsonify({"error": "Class not found"}), 404

@class_bp.route('/<class_name>/<teacher>', methods=['GET'])
def get_class_by_teacher_and_name_route(class_name, teacher):
    """Route to fetch a class by name and"""
    class_info = get_class_by_teacher_and_name(class_name, teacher)
    if class_info:
        return jsonify(process_data(class_info)), 200
    else:
        return jsonify({"error": "Class not found"}), 404
    
@class_bp.route('/allTeachers', methods=['GET'])
def get_all_professors():
    """Route to fetch all teachers"""
    teachers = get_all_teachers()
    if teachers:
        return jsonify(teachers), 200
    else:
        return jsonify({"error": "No teachers found"}), 404
