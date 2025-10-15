import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app



def test_index_redirects_to_login(client):
    response = client.get('/', follow_redirects=True)
    assert b'Iniciar sesi' in response.data

def test_404(client):
    response = client.get('/noexiste')
    assert response.status_code == 404
