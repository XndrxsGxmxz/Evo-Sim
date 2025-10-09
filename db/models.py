from datetime import datetime
from .extensiones import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(150), nullable=False)
    correo = db.Column(db.String(150), unique=True, nullable=False)
    contrasena = db.Column(db.String(200), nullable=False)
    rol = db.Column(db.String(50), nullable=False)

class Simulacion(db.Model):
    __tablename__ = 'simulaciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    beta = db.Column(db.Float, nullable=False)
    gamma = db.Column(db.Float, nullable=False)
    nombre_imagen = db.Column(db.String(255), nullable=False)
    imagen = db.Column(db.LargeBinary, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

