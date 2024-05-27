import pytest
from app import app

BASE_URL = 'http://127.0.0.1:5000/register'

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_register_successful(client):
    data = {'name':'ambikssri', 'email': 'new@randstaddigital.com', 'contact':'9456932788' ,'password': 87755443}
    response = client.post(BASE_URL, json=data)
    print(response.json)
    assert response.status_code == 201
    assert response.json['message'] == 'User registered successfully'

def test_invalid_user(client):
    data = {'name':'ambika srivastava', 'email': 'new_user@example.com', 'contact':'9456932788' ,'password':'stfgbjk'}
    response = client.post(BASE_URL, json=data)
    assert response.status_code == 401
    assert response.json['error'] == 'User already exists'

def test_register_incomplete_user(client):
    data = {'name':'', 'email': 'new_user@example.com', 'contact':'9456932788' ,'password':'stfgbjk'}
    response = client.post(BASE_URL, json=data)
    assert response.status_code == 400
    assert response.json['error'] == 'All fields input required'