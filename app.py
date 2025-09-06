from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
import os

from extensiones import db, bcrypt, login_manager
from routes_estudiante import estudiante_bp 
from routes_admin import admin_bp  # Importa el Blueprint del Administrador
from routes_investigador import investigador  # Importa el blueprint 'investigador'
from auth import auth  # Importa el blueprint 'auth'
from routes_autoridad import autoridad_bp  # Añade esta línea

def create_app():
    app = Flask(__name__)  # <-- corregido
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Juan5880#@localhost/evo_sim'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

    # Crear carpeta de uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models import Usuario, Simulacion  # Add Simulacion to the import

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.rol == 'estudiante':
                return redirect(url_for('estudiante.panel_estudiante'))
        return redirect(url_for('auth.login'))

    # Registrar Blueprints
    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')
    app.register_blueprint(investigador, url_prefix='/investigador')  # Registrar el blueprint 'investigador'
    app.register_blueprint(admin_bp)  # Blueprint para administradores
    app.register_blueprint(autoridad_bp, url_prefix='/autoridad')  # Blueprint para autoridades
    app.register_blueprint(auth, url_prefix='/auth')  # Registrar el blueprint con prefijo '/auth'

    return app

# Ejecutar la app si se llama directamente
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)