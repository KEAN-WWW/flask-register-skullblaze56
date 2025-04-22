import pytest
from application import create_app
from application.database import db, User

@pytest.fixture
def app():
    app = create_app('testing')
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_registration_page(client):
    response = client.get('/registration')
    assert response.status_code == 200

def test_dashboard_page(client):
    response = client.get('/dashboard')
    assert response.status_code == 200

def test_registration_form(app):
    with app.app_context():
        from application.bp.authentication.forms import RegistrationForm
        form = RegistrationForm()
        assert form.email is not None
        assert form.password is not None
        assert form.confirm_password is not None

def test_login_form(app):
    with app.app_context():
        from application.bp.authentication.forms import LoginForm
        form = LoginForm()
        assert form.email is not None
        assert form.password is not None
        assert form.remember is not None 