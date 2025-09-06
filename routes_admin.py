from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensiones import db, bcrypt
from models import Usuario

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def admin_panel():
    # Verificar que el usuario tenga el rol de "Administrador"
    if not current_user.is_authenticated or current_user.rol != 'Administrador':
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol')

        if not nombre or not correo or not contrasena or not rol:
            flash('Por favor, completa todos los campos.', 'error')
            return redirect(url_for('admin.admin_panel'))

        contrasena_hash = bcrypt.generate_password_hash(contrasena).decode('utf-8')
        nuevo_usuario = Usuario(
            nombre_usuario=nombre,
            correo=correo,
            contrasena=contrasena_hash,
            rol=rol
        )

        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario creado con éxito.', 'success')
        return redirect(url_for('admin.admin_panel'))

    return render_template('admin.html')