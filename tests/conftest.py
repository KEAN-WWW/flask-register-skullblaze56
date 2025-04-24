"""Test configuration module"""
import pytest
import os
from application.factory import create_app
from application.database import db, User

# Get the test database path
TEST_DB = "test.db"

@pytest.fixture(name="app")
def create_test_app():
    """create a new test app"""
    # Remove test database if it exists
    if os.path.exists(TEST_DB):
        os.unlink(TEST_DB)

    # Create app with test config
    app = create_app('testing')

    with app.app_context():
        # Create tables and yield app
        db.create_all()
        yield app
        # Clean up after test
        db.session.remove()
        if os.path.exists(TEST_DB):
            os.unlink(TEST_DB)

@pytest.fixture
def client(app):
    """Create test client with app context"""
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

def test_user_registration_duplicate_user_fail(client, app):
    """test duplicate registration"""
    print("\n=== Starting Duplicate User Test ===")
    print(f"Test Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

    with app.app_context():  # Add back the app context
        # Create first user
        user = User.create(email="steve@steve.com", password="testtest")
        db.session.add(user)
        db.session.commit()

        print("\n=== After Creating Test User ===")
        print(f"All users in database: {[u.email for u in User.query.all()]}")

        # Verify user was created
        existing_user = User.query.filter_by(email="steve@steve.com").first()
        assert existing_user is not None
        print(f"Verified user exists: {existing_user.email}")

        # Try to create duplicate user
        response = client.post("/registration", data={
            "email": "steve@steve.com",
            "password": "testtest",
            "confirm_password": "testtest",
            "submit": "Sign Up"
        }, follow_redirects=True)

        print("\n=== After Registration Attempt ===")
        print(f"Response status: {response.status_code}")
        print(f"Response path: {response.request.path}")
        print(f"All users in database: {[u.email for u in User.query.all()]}")

        # Should stay on registration page with error
        assert response.request.path == '/registration'
        assert response.status_code == 200
        assert b"That email is taken" in response.data

        # Verify only one user exists
        users = User.query.all()
        assert len(users) == 1 