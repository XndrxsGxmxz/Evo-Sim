import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from db.extensiones import db, bcrypt
from db.models import Usuario
from sqlalchemy.exc import IntegrityError

app = create_app()

with app.app_context():
    while True:
        try:
            # Solicitar datos del usuario
            nombre = input("Nombre de usuario: ")
            
            # Verificar si el usuario ya existe
            usuario_existente = Usuario.query.filter_by(nombre_usuario=nombre).first()
            if usuario_existente:
                print("❌ Error: Este nombre de usuario ya está registrado. Por favor, elija otro.")
                continue
                
            correo = input("Correo: ")
            contrasena_plana = input("Contraseña: ")
            
            # Lista de roles permitidos
            roles_validos = ['Admin', 'Investigador', 'Estudiante', 'Profesional', 'Autoridad']
            rol = input(f"Rol ({' / '.join(roles_validos)}): ").capitalize()
            
            # Validar el rol ingresado
            if rol not in roles_validos:
                print(f"❌ Error: Rol no válido. Debe ser uno de estos: {', '.join(roles_validos)}")
                continue

            # Crear hash de la contraseña
            contrasena_hash = bcrypt.generate_password_hash(contrasena_plana).decode('utf-8')

            # Crear nuevo usuario
            nuevo_usuario = Usuario(
                nombre_usuario=nombre,
                correo=correo,
                contrasena=contrasena_hash,
                rol=rol
            )

            # Guardar en la base de datos
            db.session.add(nuevo_usuario)
            db.session.commit()
            print(f"✅ Usuario '{nombre}' creado exitosamente con rol de {rol}.")
            break
            
        except IntegrityError:
            db.session.rollback()
            print("❌ Error: El correo electrónico ya está registrado en el sistema.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error inesperado: {str(e)}")
