import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from db.extensiones import db
from db.models import Usuario

def mostrar_usuarios():
    app = create_app()
    with app.app_context():
        usuarios = Usuario.query.all()
        print("\n📋 Lista de Usuarios:")
        print("=" * 50)
        for usuario in usuarios:
            print(f"ID: {usuario.id}")
            print(f"Nombre: {usuario.nombre_usuario}")
            print(f"Correo: {usuario.correo}")
            print(f"Rol: {usuario.rol}")
            print("-" * 50)

if __name__ == '__main__':
    mostrar_usuarios()