from app.config import db

class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {'autoload_with': db.engine}  # 🔥 Reflection activo

    
    tipo_cliente_id = db.Column(db.Integer, db.ForeignKey("client_types.id"), nullable=False)
    tipo_cliente = db.relationship("ClientType", backref="usuarios")
