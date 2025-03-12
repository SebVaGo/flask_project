from app.config import db

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    precio = db.Column(db.Float, nullable=False)
    categoria = db.relationship("Category", backref="productos")