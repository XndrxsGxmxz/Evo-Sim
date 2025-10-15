import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from db.extensiones import db, bcrypt
from db.models import Usuario
import unittest
import pytest

app = create_app()

@pytest.fixture(autouse=True)
def setup_admin(client):
    with client.application.app_context():
        db.create_all()
        admin = Usuario(
            nombre_usuario='admin',
            correo='admin@correo.com',
            contrasena=bcrypt.generate_password_hash('123456').decode('utf-8'),
            rol='Admin'
        )
        db.session.add(admin)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()

def login(client, correo, contrasena):
    return client.post('/auth/login', data={
        'correo': correo,
        'contrasena': contrasena
    }, follow_redirects=True)

def test_crear_usuario(client):
    login(client, 'admin@correo.com', '123456')
    response = client.post('/admin', data={
        'nombre_usuario': 'testuser',
        'correo': 'test@correo.com',
        'contrasena': '123456',
        'rol': 'Estudiante'
    }, follow_redirects=True)
    assert b'Usuario' in response.data  # Ajusta según el mensaje real
