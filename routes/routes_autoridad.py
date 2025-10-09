import os 
import json
import base64 
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
from db.extensiones import db
from db.models import Simulacion

# Cambiar el prefijo a /autoridad
autoridad_bp = Blueprint('autoridad', __name__, url_prefix='/autoridad')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png'}

# Configurar la carpeta de subida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Agregar decorator login_required y verificación de rol
@autoridad_bp.route('/')
@login_required
def home():
    # Permitir acceso tanto a admin como autoridad
    if current_user.rol not in ['Admin', 'Autoridad']:
        flash('No tienes permiso para acceder a esta página.', 'error')
        return redirect(url_for('auth.login'))
    
    simulaciones = Simulacion.query.all()
    return render_template('autoridad.html', simulaciones=simulaciones)

# Agregar verificación de rol a las demás rutas
@autoridad_bp.route('/ver_simulacion', methods=['POST'])
@login_required
def ver_simulacion():
    if current_user.rol not in ['Admin', 'Autoridad']:
        flash('No tienes permiso para acceder a esta página.', 'error')
        return redirect(url_for('auth.login'))
    
    simulacion_id = request.form.get('simulacion_id')
    simulacion = Simulacion.query.get(simulacion_id)

    if not simulacion:
        flash('Simulación no encontrada.', 'error')
        return redirect(url_for('autoridad.home'))

    # Convertir los datos binarios de la imagen a base64 para mostrarla en HTML
    import base64
    grafico_base64 = base64.b64encode(simulacion.imagen).decode('utf-8')

    return render_template('autoridad.html', simulaciones=Simulacion.query.all(), grafico=grafico_base64)

@autoridad_bp.route('/guardar_simulacion', methods=['POST'])
@login_required
def guardar_simulacion():
    # Permitir que ambos roles puedan guardar simulaciones
    if current_user.rol not in ['Admin', 'Autoridad']:
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('auth.login'))
    
    nombre_usuario = request.form.get('nombre_usuario')
    beta = request.form.get('beta')
    gamma = request.form.get('gamma')
    grafico = request.files.get('grafico')

    if not (nombre_usuario and beta and gamma and grafico):
        flash('Todos los campos son obligatorios.', 'error')
        return redirect(url_for('autoridad.home'))

    if grafico:
        # Generar un nombre único para la imagen
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        nombre_imagen = secure_filename(f"{nombre_usuario}_sim_{beta}_{gamma}_{timestamp}.png")
        
        # Leer los datos binarios de la imagen
        imagen_binaria = grafico.read()

        # Guardar la simulación en la base de datos
        nueva_simulacion = Simulacion(
            nombre_usuario=nombre_usuario,
            beta=float(beta),
            gamma=float(gamma),
            nombre_imagen=nombre_imagen,
            imagen=imagen_binaria
        )
        db.session.add(nueva_simulacion)
        db.session.commit()

        flash('Simulación guardada exitosamente.', 'success')
    else:
        flash('Error al cargar la imagen.', 'error')

    return redirect(url_for('autoridad.home'))

@autoridad_bp.route('/eliminar_simulacion', methods=['POST'])
@login_required
def eliminar_simulacion():
    # Permitir que ambos roles puedan eliminar simulaciones
    if current_user.rol not in ['Admin', 'Autoridad']:
        flash('No tienes permiso para realizar esta acción.', 'error')
        return redirect(url_for('auth.login'))
    
    simulacion_id = request.form.get('simulacion_id')
    simulacion = Simulacion.query.get(simulacion_id)

    if not simulacion:
        flash('Simulación no encontrada.', 'error')
        return redirect(url_for('autoridad.home'))

    try:
        db.session.delete(simulacion)
        db.session.commit()
        flash('Simulación eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error al eliminar la simulación.', 'error')

    return redirect(url_for('autoridad.home'))

