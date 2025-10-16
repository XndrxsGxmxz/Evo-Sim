import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from db.models import Usuario
from db.extensions import db

def test_connection():
    app = create_app()
    with app.app_context():
        try:
            # Intentar consultar usuarios
            usuarios = Usuario.query.all()
            print("\n✅ Conexión exitosa!")
            print(f"📊 Usuarios encontrados: {len(usuarios)}")
            for usuario in usuarios:
                print(f"- {usuario.nombre_usuario}")
        except Exception as e:
            print(f"\n❌ Error de conexión: {str(e)}")

if __name__ == '__main__':
    test_connection()