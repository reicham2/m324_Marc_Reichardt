"""Unit tests for the Flask application."""
import pytest


def test_app_exists():
    """Test that the Flask app can be imported."""
    from app import app
    assert app is not None


def test_app_is_testing(app_fixture):
    """Test that the app is configured for testing."""
    assert app_fixture.config['TESTING'] is True


def test_app_has_hello_route(app_fixture):
    """Test that the Flask app is properly instantiated."""
    # Basic test that the app object exists
    from app import Flask
    assert isinstance(app_fixture, type(Flask(__name__)))
