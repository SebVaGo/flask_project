from app.config import db

class OrderDetail(db.Model):
    __tablename__ = "order_details"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orden_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    
    orden = db.relationship("Order", backref="detalles")
    producto = db.relationship("Product", backref="detalles")