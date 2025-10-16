from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from db.extensions import db, bcrypt, login_manager
from routes.routes_estudiante import estudiante_bp    
from routes.routes_admin import admin_bp              
from routes.routes_investigador import investigador   
from auth import auth                                 
from routes.routes_autoridad import autoridad_bp      

def create_app():  
    app = Flask(__name__)  
    
    # Configuración desde variables de entorno
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

    # Crear carpeta de uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from db.models import Usuario, Simulacion

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
    app.register_blueprint(investigador, url_prefix='/investigador')  
    app.register_blueprint(admin_bp)                                  
    app.register_blueprint(autoridad_bp, url_prefix='/autoridad')     
    app.register_blueprint(auth, url_prefix='/auth')                  

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

