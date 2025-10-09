import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from db.extensiones import db, bcrypt
from db.models import Usuario
import unittest

app = create_app()

class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        with app.app_context():
            db.create_all()
            # Crea un usuario admin para login
            admin = Usuario(
                nombre_usuario='admin',
                correo='admin@correo.com',
                contrasena=bcrypt.generate_password_hash('123456').decode('utf-8'),
                rol='Admin'
            )
            db.session.add(admin)
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, correo, contrasena):
        return self.app.post('/auth/login', data=dict(
            correo=correo,
            contrasena=contrasena
        ), follow_redirects=True)

    def test_crear_usuario(self):
        # Primero loguea como admin
        self.login('admin@correo.com', '123456')
        # Ahora sí puedes acceder a la ruta protegida
        response = self.app.post('/admin', data=dict(
            nombre_usuario='testuser',
            correo='test@correo.com',
            contrasena='123456',
            rol='Estudiante'
        ), follow_redirects=True)
        self.assertIn(b'Usuario', response.data)  # O el mensaje flash real

if __name__ == '__main__':
    unittest.main()