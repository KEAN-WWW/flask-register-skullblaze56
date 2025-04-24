"""Testing Registration Routes"""
from flask import url_for
import pytest

from application.database import User, db
from application import create_app  # Import create_app instead of init_app

@pytest.fixture(name="app")
def create_test_app():
    """create a new test app"""
    app = create_app('testing')
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db"  # Use file-based database
    })

    with app.app_context():
        # Create tables before each test
        db.create_all()
        yield app
        # Clean up after each test
        db.session.remove()
        db.drop_all()

@pytest.fixture(name="client")
def create_client(app):
    """initialize a fixture test client for flask unit testing"""
    return app.test_client()


# def test_purify_table(app):
#     """purify the database"""
#     with app.app_context():
#         User.query.delete()
#         db.session.commit()

def test_user_registration_success(client):
    """test registration"""
    response = client.post("/registration", data={
        "email": "steve@steve.com",
        "password": "123",
        "confirm_password": "123",
        "submit": "Sign Up"
    }, follow_redirects=True)

    assert response.request.path == '/dashboard'
    assert response.status_code == 200




def test_user_registration_duplicate_user_fail(client, app):
    """test duplicate registration"""
    print("\n=== Starting Duplicate User Test ===")
    print(f"Test Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")

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
    print("\n=== Attempting Duplicate Registration ===")
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
    assert b"That email is already registered" in response.data

    # Verify only one user exists
    users = User.query.all()
    assert len(users) == 1
