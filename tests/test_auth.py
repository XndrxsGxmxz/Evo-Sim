import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture

def test_login_page_loads(client):
    response = client.get('/auth/login')
    assert response.status_code == 200
    assert b'Correo' in response.data

def test_login_invalid(client):
    response = client.post('/auth/login', data={
        'correo': 'noexiste@correo.com',
        'contrasena': 'incorrecta'
    }, follow_redirects=True)
    assert b'Correo o contrase' in response.data