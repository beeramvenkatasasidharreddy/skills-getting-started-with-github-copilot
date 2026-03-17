import pytest
from fastapi.testclient import TestClient
from src.app import app

def test_root_redirect(client: TestClient):
    """Test that root path redirects to static index"""
    # Create a client that doesn't follow redirects
    no_redirect_client = TestClient(app, follow_redirects=False)
    response = no_redirect_client.get("/")
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities(client: TestClient):
    """Test getting all activities"""
    response = client.get("/activities")
    assert response.status_code == 200

    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0

    # Check that each activity has required fields
    for name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_signup_successful(client: TestClient):
    """Test successful signup for an activity"""
    # First get current participants count
    response = client.get("/activities")
    activities = response.json()
    initial_count = len(activities["Chess Club"]["participants"])

    # Sign up a new student
    response = client.post("/activities/Chess%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 200

    result = response.json()
    assert "message" in result
    assert "test@mergington.edu" in result["message"]
    assert "Chess Club" in result["message"]

    # Verify the participant was added
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Chess Club"]["participants"]) == initial_count + 1
    assert "test@mergington.edu" in activities["Chess Club"]["participants"]

def test_signup_nonexistent_activity(client: TestClient):
    """Test signup for non-existent activity"""
    response = client.post("/activities/NonExistent/signup?email=test@mergington.edu")
    assert response.status_code == 404

    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]

def test_signup_duplicate_registration(client: TestClient):
    """Test signing up when already registered"""
    # First signup
    client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")

    # Try to signup again
    response = client.post("/activities/Chess%20Club/signup?email=duplicate@mergington.edu")
    assert response.status_code == 400

    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]

def test_unregister_successful(client: TestClient):
    """Test successful unregistration from an activity"""
    # First sign up
    client.post("/activities/Programming%20Class/signup?email=unregister@mergington.edu")

    # Get initial count
    response = client.get("/activities")
    activities = response.json()
    initial_count = len(activities["Programming Class"]["participants"])

    # Unregister
    response = client.delete("/activities/Programming%20Class/unregister/unregister@mergington.edu")
    assert response.status_code == 200

    result = response.json()
    assert "message" in result
    assert "unregister@mergington.edu" in result["message"]
    assert "Programming Class" in result["message"]

    # Verify the participant was removed
    response = client.get("/activities")
    activities = response.json()
    assert len(activities["Programming Class"]["participants"]) == initial_count - 1
    assert "unregister@mergington.edu" not in activities["Programming Class"]["participants"]

def test_unregister_nonexistent_activity(client: TestClient):
    """Test unregistering from non-existent activity"""
    response = client.delete("/activities/NonExistent/unregister/test@mergington.edu")
    assert response.status_code == 404

    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]

def test_unregister_not_registered(client: TestClient):
    """Test unregistering when not registered"""
    response = client.delete("/activities/Chess%20Club/unregister/notregistered@mergington.edu")
    assert response.status_code == 404

    result = response.json()
    assert "detail" in result
    assert "not registered" in result["detail"]