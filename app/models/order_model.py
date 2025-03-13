from app.config import db

class OrderModel(db.Model):
    __tablename__ = "orders"
    __table_args__ = {'autoload_with': db.engine}

    usuario = db.relationship("UserModel", backref="ordenes", passive_deletes=True)
    producto = db.relationship("ProductModel", backref="ordenes", passive_deletes=True)

