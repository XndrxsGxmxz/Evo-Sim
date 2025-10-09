import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
import unittest

app = create_app()

class GeneralTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_redirects_to_login(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertIn(b'Iniciar sesi', response.data)

    def test_404(self):
        response = self.app.get('/noexiste')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()