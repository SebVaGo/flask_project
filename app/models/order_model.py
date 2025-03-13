from app.config import db

class Order(db.Model):
    __tablename__ = "orders"
    __table_args__ = {'autoload_with': db.engine}  # 🔥 Reflection activo

    usuario = db.relationship("User", backref="ordenes", passive_deletes=True)
    producto = db.relationship("Product", backref="ordenes", passive_deletes=True)

