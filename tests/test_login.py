import pytest 
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_login_successful(client):
    login_url = '/login'
    login_data = {
        'email': 'ambika@gmail.com',
        'password': 12345678
    }
    response = client.post(login_url, json=login_data)
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_invalid_user(client):
    login_url = '/login'
    login_data = {
        'email': 'kilaru@gmail.com',
        'password': 'mnbvcx'
    }
    response = client.post(login_url, json=login_data)
    assert response.status_code == 401
    assert response.get_json()['error'] == 'Invalid credentials'

def test_login_incomplete_user(client):
    login_url = '/login'
    login_data = {
        'email': 'shiv@gmail.com',
        'password': ''
    }
    response = client.post(login_url, json=login_data)
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Need to fill email or password'
