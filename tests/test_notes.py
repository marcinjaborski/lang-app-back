# noinspection PyUnresolvedReferences
from . import *


def test_get_notes(client):
    response_token = client.post('/login', json={
        'username': 'johndoe',
        'password': 'qwerty123',
    })
    response = client.get('/notes', headers={'x-access-tokens': response_token.json['token']})
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['title'] == 'John note'


def test_get_notes_without_auth(client):
    response = client.get('/notes')
    assert response.status_code == 400
    assert response.json['message'] == 'a valid token is missing'


def test_get_notes_invalid_token(client):
    response = client.get('/notes', headers={
        'x-access-tokens': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIzNmEwNzBiNi1iM2ZhLTQ0ZmYtOGNkYS0xMT'
                           'g0MjljN2JlY2MiLCJleHAiOjE2NTYxNTk2MDZ9.qoyh1D0sEaPVrc9XB9_jYyqEBHwNpGZdK-j976WLdKU'
    })
    assert response.status_code == 404
    assert response.json['message'] == 'token in invalid, user does not exist'


def test_post_note(client):
    response_token = client.post('/login', json={
        'username': 'johndoe',
        'password': 'qwerty123',
    })
    response = client.post('/note', headers={'x-access-tokens': response_token.json['token']}, json={
        'title': 'New note',
        'words': 100,
        'excerpt': 'This note is new',
        'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras vitae porta nibh. Cras diam diam',
    })
    assert response.status_code == 200
    assert response.json['message'] == 'new note created'


def test_post_empty_note(client):
    response_token = client.post('/login', json={
        'username': 'johndoe',
        'password': 'qwerty123',
    })
    response = client.post('/note', headers={'x-access-tokens': response_token.json['token']}, json={})
    assert response.status_code == 200
    assert response.json['message'] == 'new note created'
