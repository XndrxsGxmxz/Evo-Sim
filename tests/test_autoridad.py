import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_panel_requires_login(client):
    response = client.get('/autoridad/', follow_redirects=True)
    assert b'Iniciar sesi' in response.data
