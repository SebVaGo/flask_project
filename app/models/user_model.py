from app.config import db

class UserModel(db.Model):
    __tablename__ = "users"
    __table_args__ = {'autoload_with': db.engine}

    
    tipo_cliente_id = db.Column(db.Integer, db.ForeignKey("client_types.id"), nullable=False)
    tipo_cliente = db.relationship("ClientTypeModel", backref="usuarios")
