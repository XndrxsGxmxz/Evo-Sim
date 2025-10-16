import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from db.models import Usuario
from db.extensions import db

def verify_data():
    app = create_app()
    with app.app_context():
        try:
            # Verificar usuarios
            usuarios = Usuario.query.all()
            print(f"\n Usuarios migrados: {len(usuarios)}")
            for usuario in usuarios:
                print(f"- {usuario.nombre_usuario} ({usuario.rol})")
        except Exception as e:
            print(f" Error: {str(e)}")

if __name__ == '__main__':
    verify_data()