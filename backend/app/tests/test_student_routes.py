import pytest
from bson.objectid import ObjectId
from flask import Flask
from app.routes.student_routes import student_bp, process_data

# Fixture to set up a test client for the Flask app
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(student_bp, url_prefix="/student")
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

# Test for GET /<student_id> (fetch student by ID)
def test_get_student(client):
    response = client.get(f"/student/{ObjectId()}")
    if response.status_code == 200:
        assert "name" in response.json  # Assuming students contain a "name" field
    elif response.status_code == 404:
        assert response.json == {"error": "Student not found"}

# Test for GET /fid/<student_fid> (fetch student by fid)
def test_get_student_fid(client):
    student_fid = "12345"  # Replace with an actual fid or a test fid value
    response = client.get(f"/student/fid/{student_fid}")
    if response.status_code == 200:
        assert "name" in response.json  # Assuming students contain a "name" field
    elif response.status_code == 404:
        assert response.json == {"error": "Student not found"}

# Test for POST / (create a new student)
def test_add_student(client):
    response = client.post("/student/", json={
        "fid": "12345",
        "name": "John Doe",
        "age": 20,
        "major": "Computer Science"
    })
    if response.status_code == 201:
        assert "id" in response.json
        assert response.json["message"] == "Student created"
    elif response.status_code == 400:
        assert response.json == {"error": "Error creating student"}

# Test for PUT /<student_id> (update a student)
def test_edit_student(client):
    response = client.put(f"/student/{ObjectId()}", json={
        "name": "Jane Doe",
        "age": 21
    })
    if response.status_code == 200:
        assert response.json == {"message": "Student updated"}
    elif response.status_code == 400:
        assert response.json == {"error": "No changes made"}

# Test for DELETE /<student_id> (delete a student)
def test_remove_student(client):
    response = client.delete(f"/student/{ObjectId()}")
    if response.status_code == 200:
        assert response.json == {"message": "Student deleted"}
    elif response.status_code == 404:
        assert response.json == {"error": "Student not found"}
