import os
import sys
import uuid
import requests

BASE_URL = os.getenv('BASE_URL')

def uuid_hex():
    return uuid.uuid4().hex

email = 'admin-%s@example.com' % uuid_hex()
user = {'email': email, 'password': '123'}

def test_api():
    register_url = BASE_URL + '/register'
    response = requests.post(register_url, json={'user': user})
    assert response.status_code == 201
    body = response.json()
    assert body['user']['email'] == email
    assert body['user']['recent_successful_logins'] == []

    login_url = BASE_URL + '/login'
    response = requests.post(login_url, json=user)
    assert response.status_code == 200
    token = response.json()['token']
    assert token
