from flask_login import UserMixin
from sqlalchemy import Column, Integer
from app.config import db

class UserModel(db.Model, UserMixin):
    __tablename__ = "users"
    __table_args__ = {'autoload_with': db.engine}

    id = Column(Integer, primary_key=True)

    tipo_cliente_id = db.Column(db.Integer, db.ForeignKey("client_types.id"), nullable=False)
    tipo_cliente = db.relationship("ClientTypeModel", backref="usuarios")

    @property
    def is_active(self):
        return self.status == "activo"
    
    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No hay un ID disponible')