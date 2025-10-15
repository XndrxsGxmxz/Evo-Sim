import pytest
from db.models import Usuario
from db.extensiones import db

@pytest.fixture(autouse=True)
def setup_db(client):
    with client.application.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()

def test_usuario_creation(client):
    with client.application.app_context():
        usuario = Usuario(nombre_usuario='test', correo='test@correo.com', contrasena='123', rol='Estudiante')
        db.session.add(usuario)
        db.session.commit()
        assert Usuario.query.filter_by(correo='test@correo.com').first() is not None
