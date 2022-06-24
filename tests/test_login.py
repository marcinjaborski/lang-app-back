# noinspection PyUnresolvedReferences
from . import *
import jwt


def test_signup(client, app):
    response = client.post('/sign-up', json={
        'username': 'johnsmith',
        'email': 'john.smith@example.com',
        'password': 'qwerty123',
    })
    assert response.status_code == 200
    assert response.json.get('token')
    data = jwt.decode(response.json['token'], app.config['SECRET_KEY'], algorithms=["HS256"])
    assert data.get('public_id')
    assert data.get('exp')


def test_signup_existing_email(client):
    response = client.post('/sign-up', json={
        'username': 'newUsername',
        'email': 'john.doe@example.com',
        'password': 'qwerty123',
    })
    assert response.status_code == 400
    assert response.json['message'] == 'This email address is already in use'


def test_signup_existing_username(client):
    response = client.post('/sign-up', json={
        'username': 'johndoe',
        'email': 'newEmail@examle.com',
        'password': 'qwerty123',
    })
    assert response.status_code == 400
    assert response.json['message'] == 'This username address is already in use'


def test_signup_missing_attributes(client):
    response = client.post('/sign-up', json={})
    assert response.status_code == 400
    assert response.json['message'] == 'Missing attributes'


def test_login(client, app):
    response = client.post('/login', json={
        'username': 'johndoe',
        'password': 'qwerty123',
    })
    assert response.status_code == 200
    assert response.json.get('token')
    data = jwt.decode(response.json['token'], app.config['SECRET_KEY'], algorithms=["HS256"])
    assert data.get('public_id')
    assert data.get('exp')


def test_login_invalid_username(client):
    response = client.post('/login', json={
        'username': 'invalid',
        'password': 'qwerty123',
    })
    assert response.status_code == 404
    assert response.json['message'] == 'User does not exist'


def test_login_invalid_password(client):
    response = client.post('/login', json={
        'username': 'johndoe',
        'password': 'invalid',
    })
    assert response.status_code == 404
    assert response.json['message'] == 'Wrong password'


def test_login_missing_attributes(client):
    response = client.post('/login', json={})
    assert response.status_code == 400
    assert response.json['message'] == 'Missing arguments'
