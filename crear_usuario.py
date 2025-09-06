from app import create_app, db, bcrypt
from models import Usuario

app = create_app()

with app.app_context():
    nombre = input("Nombre de usuario: ")
    correo = input("Correo: ")
    contrasena_plana = input("Contraseña: ")
    rol = input("Rol (Administrador / Investigador / Estudiante / Profesional / Autoridad): ")

    contrasena_hash = bcrypt.generate_password_hash(contrasena_plana).decode('utf-8')

    nuevo_usuario = Usuario(
        nombre_usuario=nombre,
        correo=correo,
        contrasena=contrasena_hash,
        rol=rol
    )

    db.session.add(nuevo_usuario)
    db.session.commit()
    print("✅ Usuario creado con éxito.")
