from app.config import db
from app.models.product_model import Product
from app.models.categoy_product_model import Category
from app.models.order_model import Order

class ProductService:
    def __init__(self):
        self.db = db

    def get_all_categories(self):
        return Category.query.all()

    def create_product(self, data):
        categoria = Category.query.get(data["categoria_id"])
        if not categoria:
            return {"success": False, "message": "Categoría no válida"}

        product = Product(
            nombre=data["nombre"],
            categoria_id=data["categoria_id"],
            precio=data["precio"]
        )

        try:
            self.db.session.add(product)
            self.db.session.commit()
            return {"success": True, "message": "Producto creado exitosamente"}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al crear el producto: {str(e)}"}

    def get_all_products(self):
        return (
            Product.query.join(Category)
            .add_columns(
                Product.id,
                Product.nombre,
                Product.precio,
                Category.nombre.label("categoria")
            )
            .all()
        )

    def delete_product(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}

        orders_linked = Order.query.filter_by(producto_id=product_id).count()
        if orders_linked > 0:
            return {
                "success": False, 
                "message": "No se puede eliminar el producto, está asociado a órdenes existentes."
            }

        try:
            self.db.session.delete(product)
            self.db.session.commit()
            return {"success": True, "message": "Producto eliminado exitosamente"}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al eliminar el producto: {str(e)}"}

    def get_product_by_id(self, product_id):
        return Product.query.get(product_id)

    def update_product(self, product_id, data):
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}

        try:
            product.nombre = data["nombre"]
            product.categoria_id = data["categoria_id"]
            product.precio = data["precio"]

            self.db.session.commit()
            return {"success": True, "message": "Producto actualizado exitosamente"}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al actualizar el producto: {str(e)}"}
