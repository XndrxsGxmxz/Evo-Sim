from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, logout_user, login_required
from db.extensions import db, bcrypt
from db.models import Usuario

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
        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario and bcrypt.check_password_hash(usuario.contrasena, contrasena):
            login_user(usuario)
            session['usuario'] = usuario.nombre_usuario
            session['rol'] = usuario.rol
            
            # Redirección según el rol
            if usuario.rol == 'Admin':
                return redirect(url_for('admin.home'))
            elif usuario.rol == 'Investigador':
                return redirect(url_for('investigador.panel_investigador'))
            elif usuario.rol == 'Estudiante':
                return redirect(url_for('estudiante.panel_estudiante'))
            elif usuario.rol == 'Autoridad':
                return redirect(url_for('autoridad.home'))
            else:
                flash('Rol no reconocido.', 'error')
                return redirect(url_for('auth.login'))
        
        # Si las credenciales son incorrectas
        flash('Correo o contraseña incorrectos.', 'error')
        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'success')
    return redirect(url_for('auth.login'))
