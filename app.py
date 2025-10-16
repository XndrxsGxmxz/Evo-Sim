from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
import os

from db.extensions import db, bcrypt, login_manager
from routes.routes_estudiante import estudiante_bp    # Importa el Blueprint del Estudiante
from routes.routes_admin import admin_bp              # Importa el Blueprint del Administrador
from routes.routes_investigador import investigador   # Importa el blueprint 'investigador'
from auth import auth                                 # Importa el blueprint 'auth'
from routes.routes_autoridad import autoridad_bp      # Importa el Blueprint de Autoridades

def create_app():  # Función para crear la app
    app = Flask(__name__)  
    app.config['SECRET_KEY'] = 'Juan5880#'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Juan5880%23@evo-sim-db.cnsa0oc4az74.us-east-2.rds.amazonaws.com:5432/evo_sim_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

    # Crear carpeta de uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from db.models import Usuario, Simulacion # Importar modelos aquí para evitar problemas de circularidad 

    @login_manager.user_loader   # Función para cargar el usuario
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.route('/')  # Ruta raíz
    def index():
        if current_user.is_authenticated:
            if current_user.rol == 'estudiante':
                return redirect(url_for('estudiante.panel_estudiante'))
        return redirect(url_for('auth.login'))

    # Registrar Blueprints
    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')   # Registrar el Blueprint del Estudiante
    app.register_blueprint(investigador, url_prefix='/investigador')  # Registrar el blueprint 'investigador'
    app.register_blueprint(admin_bp)                                  # Registrar el Blueprint para administradores
    app.register_blueprint(autoridad_bp, url_prefix='/autoridad')     # Registrar el Blueprint para autoridades
    app.register_blueprint(auth, url_prefix='/auth')                  # Registrar el blueprint con prefijo '/auth'

    return app

# Ejecutar la app si se llama directamente
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

    