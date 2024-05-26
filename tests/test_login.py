import pytest
from Effort_Estimation_Tool_Capstone.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:s
        yield client

def test_register_user(client):
    register_url = '/register'
    register_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'contact': '1234567890',
        'password': 'password123'
    }
    response = client.post(register_url, json=register_data)
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_login_successful(client):
    # First register the user
    register_url = '/register'
    register_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'contact': '1234567890',
        'password': 'password123'
    }
    client.post(register_url, json=register_data)

    # Now attempt to login
    login_url = '/login'
    login_data = {
        'email': 'john.doe@example.com',
        'password': 'password123'
    }
    response = client.post(login_url, json=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_invalid_user(client):
    login_url = '/login'
    login_data = {
        'email': 'invalid.email@example.com',
        'password': 'wrongpassword'
    }
    response = client.post(login_url, json=login_data)
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid credentials'

def test_login_incomplete_user(client):
    login_url = '/login'
    login_data = {
        'email': 'john.doe@example.com'
        # missing password
    }
    response = client.post(login_url, json=login_data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Missing fields'
