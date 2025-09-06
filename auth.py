from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user
from extensiones import db, bcrypt
from models import Usuario

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')

        # Validación básica de entrada
        if not correo or not contrasena:
            flash('Por favor, completa todos los campos.', 'error')
            return redirect(url_for('auth.login'))

        # Buscar usuario en la base de datos
        user = Usuario.query.filter_by(correo=correo).first()
        if user and bcrypt.check_password_hash(user.contrasena, contrasena):
            login_user(user)
            session['usuario'] = user.nombre_usuario
            session['rol'] = user.rol
            return redirect(f'/{user.rol.lower()}')
        
        # Si las credenciales son incorrectas
        flash('Correo o contraseña incorrectos.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('login.html')
