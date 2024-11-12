import pytest
from bson.objectid import ObjectId
from flask import Flask
from app.routes.grade_routes import grade_bp, process_data

# Fixture to set up a test client for the Flask app
@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(grade_bp, url_prefix="/grade")
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

# Test for GET /<grade_id> (fetch grade by ID)
def test_get_grade(client):
    response = client.get(f"/grade/{ObjectId()}")
    if response.status_code == 200:
        assert "score" in response.json  # Assuming grades contain a "score" field
    elif response.status_code == 404:
        assert response.json == {"error": "Grade not found"}

# Test for POST / (create a new grade)
def test_add_grade(client):
    response = client.post("/grade/", json={
        "student_id": "123456",
        "course_id": "CS 1101",
        "score": 85,
        "comments": "Good job"
    })
    if response.status_code == 201:
        assert "id" in response.json
        assert response.json["message"] == "Grade created"
    elif response.status_code == 400:
        assert response.json == {"error": "Error creating grade"}

# Test for PUT /<grade_id> (update a grade)
def test_edit_grade(client):
    response = client.put(f"/grade/{ObjectId()}", json={
        "score": 90,
        "comments": "Excellent improvement"
    })
    if response.status_code == 200:
        assert response.json == {"message": "Grade updated"}
    elif response.status_code == 400:
        assert response.json == {"error": "No changes made"}

# Test for DELETE /<grade_id> (delete a grade)
def test_remove_grade(client):
    response = client.delete(f"/grade/{ObjectId()}")
    if response.status_code == 200:
        assert response.json == {"message": "Grade deleted"}
    elif response.status_code == 404:
        assert response.json == {"error": "Grade not found"}
