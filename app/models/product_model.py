from app.config import db

class Product(db.Model):
    __tablename__ = "products"
    __table_args__ = {'autoload_with': db.engine}  # Reflection automático

    categoria = db.relationship("Category", backref="productos")
