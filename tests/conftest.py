"""Pytest configuration and fixtures for the FastAPI tests."""

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

# Add src directory to path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test."""
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn and play tennis with fellow students",
            "schedule": "Saturdays, 10:00 AM - 12:00 PM",
            "max_participants": 8,
            "participants": ["james@mergington.edu", "sarah@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays and theatrical productions",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["charlotte@mergington.edu"]
        },
        "Debate Team": {
            "description": "Compete in debate competitions and develop argumentation skills",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["noah@mergington.edu", "ava@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Participate in science competitions and experiments",
            "schedule": "Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["mason@mergington.edu"]
        }
    }
    
    # Clear and restore activities
    activities.clear()
    activities.update(initial_state)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(initial_state)
