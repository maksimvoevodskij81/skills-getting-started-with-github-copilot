import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    """Test retrieving all activities."""
    # Arrange: No special setup needed (app has default data)
    
    # Act: Make the GET request
    response = client.get("/activities")
    
    # Assert: Check status and response structure
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]

def test_signup_success():
    """Test successful signup for an activity."""
    # Arrange: Define test email
    email = "newstudent@mergington.edu"
    
    # Act: Perform signup
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Assert: Check response and data update
    assert response.status_code == 200
    result = response.json()
    assert "Signed up" in result["message"]
    # Verify participant added
    response = client.get("/activities")
    data = response.json()
    assert email in data["Chess Club"]["participants"]

def test_signup_duplicate():
    """Test signing up with an email already registered."""
    # Arrange: Sign up once first
    email = "dupstudent@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Act: Attempt duplicate signup
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Assert: Check for error
    assert response.status_code == 400
    result = response.json()
    assert "already signed up" in result["detail"]

def test_signup_activity_not_found():
    """Test signing up for a non-existent activity."""
    # Arrange: Use invalid activity name
    email = "test@mergington.edu"
    
    # Act: Attempt signup
    response = client.post("/activities/Nonexistent Activity/signup", params={"email": email})
    
    # Assert: Check for not found error
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_delete_success():
    """Test successful unregistration from an activity."""
    # Arrange: Sign up first
    email = "deleteme@mergington.edu"
    client.post("/activities/Chess Club/signup", params={"email": email})
    
    # Act: Perform deletion
    response = client.delete("/activities/Chess Club/signup", params={"email": email})
    
    # Assert: Check response and data update
    assert response.status_code == 200
    result = response.json()
    assert "Unregistered" in result["message"]
    # Verify participant removed
    response = client.get("/activities")
    data = response.json()
    assert email not in data["Chess Club"]["participants"]

def test_delete_not_signed_up():
    """Test deleting a participant not signed up."""
    # Arrange: Use email not signed up
    email = "notsigned@mergington.edu"
    
    # Act: Attempt deletion
    response = client.delete("/activities/Chess Club/signup", params={"email": email})
    
    # Assert: Check for error
    assert response.status_code == 404
    result = response.json()
    assert "not signed up" in result["detail"]

def test_delete_activity_not_found():
    """Test deleting from a non-existent activity."""
    # Arrange: Use invalid activity name
    email = "test@mergington.edu"
    
    # Act: Attempt deletion
    response = client.delete("/activities/Nonexistent Activity/signup", params={"email": email})
    
    # Assert: Check for not found error
    assert response.status_code == 404
    result = response.json()
    assert "Activity not found" in result["detail"]

def test_root_redirect():
    """Test root endpoint redirects to static index."""
    # Arrange: No setup needed
    
    # Act: Make GET request without following redirects
    response = client.get("/", follow_redirects=False)
    
    # Assert: Check redirect status and location
    assert response.status_code == 307
    assert "/static/index.html" in response.headers["location"]