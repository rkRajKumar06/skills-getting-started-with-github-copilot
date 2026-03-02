import pytest
from fastapi.testclient import TestClient
from src.app import app

@pytest.fixture
def client():
    """Fixture for FastAPI test client."""
    return TestClient(app)
