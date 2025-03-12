from app.config import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    cliente = db.relationship("User", backref="ordenes")