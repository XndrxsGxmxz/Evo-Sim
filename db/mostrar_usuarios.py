# mostrar_usuarios.py
from app import create_app
from models import Usuario
from extensiones import db

app = create_app()
with app.app_context():
    usuarios = Usuario.query.all()
    for u in usuarios:
        print(f"{u.id} | {u.nombre_usuario} | {u.correo} | {u.rol}")