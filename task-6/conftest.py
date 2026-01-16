"""Pytest configuration and fixtures."""
import pytest


@pytest.fixture
def app_fixture():
    """Create a test fixture for the Flask app."""
    from app import app
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app_fixture):
    """Create a test client for the Flask app."""
    return app_fixture.test_client()
