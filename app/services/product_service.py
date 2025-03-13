# product_service.py
from app.config import db
from app.models.product_model import Product
from app.models.categoy_product_model import Category
from sqlalchemy import update

class ProductService:
    def __init__(self):
        self.db = db

    def get_all_categories(self):
        return Category.query.all()

    def create_product(self, data):
        categoria = Category.query.get(data["categoria_id"])
        if not categoria:
            return {"success": False, "message": "Categoría no válida"}

        try:
            product = Product(**data)
            db.session.add(product)
            db.session.commit()
            return {"success": True, "message": "Producto creado exitosamente"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Error al crear el producto: {str(e)}"}

    def get_all_products(self):
        return db.session.query(
            Product.id,
            Product.nombre,
            Product.precio,
            Category.nombre.label("categoria")
        ).join(Category).all()

    def get_product_by_id(self, product_id):
        return db.session.query(
            Product.id,
            Product.categoria_id,
            Category.nombre.label("categoria"),
            Product.nombre,
            Product.precio
        ).join(Category).filter(Product.id == product_id).first()

    def update_product(self, product_id, data):
        try:
            db.session.execute(
                update(Product)
                .where(Product.id == product_id)
                .values(**data)
            )
            db.session.commit()
            return {"success": True, "message": "Producto actualizado exitosamente"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": f"Error al actualizar el producto: {str(e)}"}

    def delete_product(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}
        try:
            self.db.session.delete(product)
            self.db.session.commit()
            return {"success": True, "message": "Producto eliminado"}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al eliminar el producto: {str(e)}"}
