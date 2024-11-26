import pytest
from bson.objectid import ObjectId
from flask import Flask
from app.routes.class_routes import class_bp, process_data

# Fixture to set up a test client for the Flask app
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(class_bp, url_prefix="/class")
    return app.test_client()

def test_process_data_with_objectid():
    data = {
        "id": ObjectId("507f1f77bcf86cd799439011"),
        "name": "Test Item"
    }
    result = process_data(data)
    assert result["id"] == "507f1f77bcf86cd799439011"
    assert result["name"] == "Test Item"

def test_process_data_with_nested_objectid_list():
    data = {
        "ids": [ObjectId("507f1f77bcf86cd799439011"), ObjectId("507f1f77bcf86cd799439012")],
        "name": "Test Item"
    }
    result = process_data(data)
    assert result["ids"] == ["507f1f77bcf86cd799439011", "507f1f77bcf86cd799439012"]
    assert result["name"] == "Test Item"

# Test for GET /<class_id> (fetch class by ID)
def test_get_class(client):
    response = client.get(f"/class/{ObjectId()}")
    if response.status_code == 200:
        assert "name" in response.json
    elif response.status_code == 404:
        assert response.json == {"error": "Class not found"}

# Test for POST / (create a new class)
def test_add_class(client):
    response = client.post("/class/", json={
        "code": "CS 1101",
        "name": "Introduction to CS",
        "description": "Basic CS concepts",
        "teacher": "SMITH, J",
        "grades": []
    })
    if response.status_code == 201:
        assert "id" in response.json
        assert response.json["message"] == "Class created"
    elif response.status_code == 400:
        assert response.json == {"error": "Error creating class"}
    
    response = client.delete(f"/class/{response.json['id']}")

# Test for PUT /<class_id> (update a class)
def test_edit_class(client):
    response = client.put(f"/class/{ObjectId()}", json={
        "name": "Updated CS Course",
        "teacher": "JOHNSON, M"
    })
    if response.status_code == 200:
        assert response.json == {"message": "Class updated"}
    elif response.status_code == 400:
        assert response.json == {"error": "No changes made"}

# Test for DELETE /<class_id> (delete a class)
def test_remove_class(client):
    response = client.delete(f"/class/{ObjectId()}")
    if response.status_code == 200:
        assert response.json == {"message": "Class deleted"}
    elif response.status_code == 404:
        assert response.json == {"error": "Class not found"}

# Test for GET / (fetch all classes)
def test_get_classes(client):
    response = client.get("/class/")
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Expected a list of classes

# Test for GET /<class_name>/teachers (fetch all teachers for a class)
def test_get_teachers(client):
    response = client.get("/class/Physics/teachers")
    if response.status_code == 200:
        assert isinstance(response.json, list)  # Expected a list of teachers
    elif response.status_code == 404:
        assert response.json == {"error": "Class not found"}

# Test for GET /<class_name>/<teacher> (fetch class by name and teacher)
def test_get_class_by_teacher_and_name(client):
    response = client.get("/class/Physics/John Doe")
    if response.status_code == 200:
        assert "name" in response.json
        assert response.json["name"] == "Physics"
    elif response.status_code == 404:
        assert response.json == {"error": "Class not found"}

# Test for GET /allTeachers (fetch all teachers)
def test_get_all_professors(client):
    response = client.get("/class/allTeachers")
    if response.status_code == 200:
        assert isinstance(response.json, list)  # Expected a list of teachers
    elif response.status_code == 404:
        assert response.json == {"error": "No teachers found"}
