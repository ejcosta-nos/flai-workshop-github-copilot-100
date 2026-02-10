"""Test cases for the FastAPI application."""

import pytest


class TestActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all available activities."""
        response = client.get("/activities")
        
        assert response.status_code == 200
        data = response.json()
        
        # Check that all activities are present
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
        assert "Basketball Team" in data
        assert "Tennis Club" in data
        assert "Drama Club" in data
        assert "Art Studio" in data
        assert "Debate Team" in data
        assert "Science Olympiad" in data

    def test_activities_have_required_fields(self, client, reset_activities):
        """Test that each activity has required fields."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_activities_have_correct_participant_count(self, client, reset_activities):
        """Test that activities have the correct initial participant counts."""
        response = client.get("/activities")
        data = response.json()
        
        # Check a few known activities
        assert len(data["Chess Club"]["participants"]) == 2
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Basketball Team"]["participants"]) == 1


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_for_activity_success(self, client, reset_activities):
        """Test successful signup for an activity."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "newstudent@mergington.edu" in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        """Test that signup actually adds the participant to the activity."""
        email = "newstudent@mergington.edu"
        
        # Signup
        response = client.post(
            f"/activities/Chess%20Club/signup?email={email}"
        )
        assert response.status_code == 200
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data["Chess Club"]["participants"]

    def test_signup_for_nonexistent_activity(self, client, reset_activities):
        """Test that signup fails for a non-existent activity."""
        response = client.post(
            "/activities/Nonexistent%20Activity/signup?email=student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_already_registered_student(self, client, reset_activities):
        """Test that signup fails if student is already registered."""
        response = client.post(
            "/activities/Chess%20Club/signup?email=michael@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"]

    def test_signup_multiple_students(self, client, reset_activities):
        """Test that multiple students can sign up for the same activity."""
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        response1 = client.post(
            f"/activities/Chess%20Club/signup?email={email1}"
        )
        response2 = client.post(
            f"/activities/Chess%20Club/signup?email={email2}"
        )
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        activities_response = client.get("/activities")
        participants = activities_response.json()["Chess Club"]["participants"]
        assert email1 in participants
        assert email2 in participants


class TestUnregisterEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants/{email} endpoint."""

    def test_unregister_participant_success(self, client, reset_activities):
        """Test successful unregistration of a participant."""
        response = client.delete(
            "/activities/Chess%20Club/participants/michael@mergington.edu"
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]

    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister actually removes the participant."""
        email = "michael@mergington.edu"
        
        # Unregister
        response = client.delete(
            f"/activities/Chess%20Club/participants/{email}"
        )
        assert response.status_code == 200
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        participants = activities_response.json()["Chess Club"]["participants"]
        assert email not in participants

    def test_unregister_from_nonexistent_activity(self, client, reset_activities):
        """Test that unregister fails for a non-existent activity."""
        response = client.delete(
            "/activities/Nonexistent%20Activity/participants/student@mergington.edu"
        )
        
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_unregister_nonexistent_participant(self, client, reset_activities):
        """Test that unregister fails if participant is not signed up."""
        response = client.delete(
            "/activities/Chess%20Club/participants/nonexistent@mergington.edu"
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Participant not found" in data["detail"]

    def test_unregister_all_participants(self, client, reset_activities):
        """Test that all participants can be unregistered."""
        activity = "Basketball Team"
        
        # Get initial participants
        activities_response = client.get("/activities")
        participants = list(activities_response.json()[activity]["participants"])
        
        # Unregister all
        for participant in participants:
            response = client.delete(
                f"/activities/{activity}/participants/{participant}"
            )
            assert response.status_code == 200
        
        # Verify all were removed
        activities_response = client.get("/activities")
        remaining = activities_response.json()[activity]["participants"]
        assert len(remaining) == 0
