from app.config import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primer_nombre = db.Column(db.String(50), nullable=False)
    segundo_nombre = db.Column(db.String(50), nullable=True)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="activo")
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    tipo_cliente_id = db.Column(db.Integer, db.ForeignKey("client_types.id"), nullable=False)
    tipo_cliente = db.relationship("ClientType", backref="usuarios")


    def __repr__(self):
        return f"<User {self.correo}>"

from app.models.associations_model import *