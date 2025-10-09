import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
import unittest

app = create_app()

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_login_page_loads(self):
        response = self.app.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Correo', response.data)

    def login(self, correo, contrasena):
        return self.app.post('/auth/login', data=dict(
            correo=correo,
            contrasena=contrasena
        ), follow_redirects=True)

if __name__ == '__main__':
    unittest.main()