from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from extensiones import db, bcrypt, login_manager
from routes_estudiante import estudiante_bp 
from routes_admin import admin_bp  # Importa el Blueprint del Administrador
from routes_investigador import investigador  # Importa el blueprint 'investigador'
from auth import auth  # Importa el blueprint 'auth'

def create_app():
    app = Flask(__name__)  # <-- corregido
    app.config['SECRET_KEY'] = 'tu_clave_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Juan5880#@localhost/evo_sim'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from models import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))  # Redirige a la página de inicio de sesión

    # Registrar Blueprints
    app.register_blueprint(estudiante_bp, url_prefix='/estudiante')
    app.register_blueprint(investigador, url_prefix='/investigador')  # Registrar el blueprint 'investigador'
    app.register_blueprint(admin_bp, url_prefix='/admin')  # Registrar el Blueprint del Administrador
    app.register_blueprint(auth, url_prefix='/auth')  # Registrar el blueprint con prefijo '/auth'

    return app

# Ejecutar la app si se llama directamente
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)