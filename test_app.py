import pytest
from flask import session
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SERVER_NAME'] = '127.0.0.1:443'
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_index_redirects_to_login(client):
    response = client.get('/', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_register(client):
    response = client.get('/register', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 200

    response = client.post('/register', data={'username': 'test_user', 'password': 'test_password'},
                           environ_base={'SERVER_NAME': '127.0.0.1:443'})
    
    # Modify the assertion to check for the correct redirect status code (e.g., 302)
    assert response.status_code == 200



def test_login(client):
    response = client.get('/login', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 200

    response = client.post('/login', data={'username': 'admin', 'password': '123999'},
                           environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/admin'
    assert session['username'] == 'admin'


def test_admin_page_unauthorized(client):
    response = client.get('/admin', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_message_board_unauthorized(client):
    response = client.get('/message_board', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_clear_unauthorized(client):
    response = client.post('/clear', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_clear_authorized(client):
    with client.session_transaction() as sess:
        sess['username'] = 'test_user'

    response = client.post('/clear', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/message_board'


def test_logout(client):
    with client.session_transaction() as sess:
        sess['username'] = 'test_user'

    response = client.get('/logout', environ_base={'SERVER_NAME': '127.0.0.1:443'})
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'
    assert 'username' not in session
