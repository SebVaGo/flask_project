from app.config import db
from datetime import datetime

class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orden_id = db.Column(db.Integer, nullable=False)  # 🔹 ID único por compra
    usuario_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_actualizacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    usuario = db.relationship("User", backref="ordenes", passive_deletes=True)
    producto = db.relationship("Product", backref="ordenes", passive_deletes=True)
