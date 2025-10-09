import unittest
from db.models import Usuario
from db.extensiones import db
from app import create_app

app = create_app()

class ModelsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_usuario_creation(self):
        usuario = Usuario(nombre_usuario='test', correo='test@correo.com', contrasena='123', rol='Estudiante')
        db.session.add(usuario)
        db.session.commit()
        self.assertIsNotNone(Usuario.query.filter_by(correo='test@correo.com').first())

if __name__ == '__main__':
    unittest.main()