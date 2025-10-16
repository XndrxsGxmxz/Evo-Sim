from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from db.models import Usuario
from db.extensions import db, bcrypt

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin', methods=['GET', 'POST'])  # Añadir POST al método
@login_required
def home():
    if current_user.rol != 'Admin':
        flash('No tienes permiso para acceder a esta página.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form.get('nombre')
        correo = request.form.get('correo')
        contrasena = request.form.get('contrasena')
        rol = request.form.get('rol')
        
        # Validar que no exista el usuario
        if Usuario.query.filter_by(nombre_usuario=nombre).first():
            flash('El nombre de usuario ya existe.', 'error')
            return redirect(url_for('admin.home'))
        
        # Crear nuevo usuario
        try:
            hashed_password = bcrypt.generate_password_hash(contrasena).decode('utf-8')
            nuevo_usuario = Usuario(
                nombre_usuario=nombre,
                correo=correo,
                contrasena=hashed_password,
                rol=rol
            )
            db.session.add(nuevo_usuario)
            db.session.commit()
            flash(f'Usuario {nombre} creado exitosamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Error al crear el usuario.', 'error')
    
    usuarios = Usuario.query.all()
    return render_template('admin.html', usuarios=usuarios)

@admin_bp.route('/eliminar_usuario/<int:user_id>', methods=['POST'])
@login_required
def eliminar_usuario(user_id):
    if current_user.rol != 'Admin':
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('index'))
    
    usuario = Usuario.query.get_or_404(user_id)
    if usuario.rol == 'Admin' and usuario.id == current_user.id:
        flash('No puedes eliminar tu propia cuenta de administrador.', 'error')
        return redirect(url_for('admin.home'))
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash(f'Usuario {usuario.nombre_usuario} eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar el usuario.', 'error')
    
    return redirect(url_for('admin.home'))