import pytest

# AAA: Arrange-Act-Assert pattern used in all tests

def test_get_activities(client):
    # Arrange
    # (client fixture provides app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0

def test_signup_activity(client):
    # Arrange
    activity_name = next(iter(client.get("/activities").json().keys()))
    email = "testuser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    # Confirm participant is added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_prevent_duplicate_signup(client):
    # Arrange
    activity_name = next(iter(client.get("/activities").json().keys()))
    email = "dupeuser@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_unregister_activity(client):
    # Arrange
    activity_name = next(iter(client.get("/activities").json().keys()))
    email = "removeuser@mergington.edu"
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    # Confirm participant is removed
    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]

def test_activity_not_found(client):
    # Arrange
    activity_name = "nonexistent"
    email = "nouser@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]
