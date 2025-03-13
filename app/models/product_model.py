from app.config import db

class ProductModel(db.Model):
    __tablename__ = "products"
    __table_args__ = {'autoload_with': db.engine} 

    categoria = db.relationship("CategoryModel", backref="productos")
