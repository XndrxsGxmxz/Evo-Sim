import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
import unittest

app = create_app()

class AutoridadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_panel_requires_login(self):
        response = self.app.get('/autoridad/', follow_redirects=True)
        self.assertIn(b'Iniciar sesi', response.data)

    # Para testear POST necesitas un usuario logueado, así que este test
    # solo funcionará si simulas login o mockeas el login.

if __name__ == '__main__':
    unittest.main()