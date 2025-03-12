from app.config import db
from app.models.product_model import Product
from app.models.categoy_product_model import Category

class ProductService:
    @staticmethod
    def get_all_categories():
        """Obtiene todas las categorías de productos"""
        categories = Category.query.all()
        print("Categorías encontradas:", categories)  # 🔹 DEBUG
        return categories
    
    @staticmethod
    def create_product(data):
        categoria = Category.query.get(data["categoria_id"])
        if not categoria:
            return {"success": False, "message": "Categoría no válida"}

        product = Product(
            nombre=data["nombre"],
            categoria_id=data["categoria_id"],
            precio=data["precio"]
        )

        db.session.add(product)
        db.session.commit()

        return {"success": True, "message": "Producto creado exitosamente"}

    @staticmethod
    def get_all_products():
        """Obtiene todos los productos"""
        return Product.query.join(Category).add_columns(Product.id, Product.nombre, Product.precio, Category.nombre.label("categoria")).all()

    @staticmethod
    def delete_product(product_id):
        """Elimina un producto por su ID"""
        product = Product.query.get(product_id)
        if not product:
            print(f"Producto con ID {product_id} no encontrado")  # 🔹 DEBUG
            return {"success": False, "message": "Producto no encontrado"}

        try:
            db.session.delete(product)
            db.session.commit()
            return {"success": True, "message": "Producto eliminado exitosamente"}
        except Exception as e:
            db.session.rollback()
            print(f"Error eliminando producto: {e}")  # 🔹 DEBUG
            return {"success": False, "message": "Error al eliminar el producto"}
    
    @staticmethod
    def get_product_by_id(product_id):
        """Obtiene un producto por su ID"""
        product = Product.query.get(product_id)
        if not product:
            print(f"Producto con ID {product_id} no encontrado")  # 🔹 DEBUG
            return None

        return product
    
    @staticmethod
    def update_product(product_id, data):
        """Actualiza un producto existente"""
        product = Product.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}

        try:
            product.nombre = data["nombre"]
            product.categoria_id = data["categoria_id"]
            product.precio = data["precio"]

            db.session.commit()
            return {"success": True, "message": "Producto actualizado exitosamente"}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "message": "Error al actualizar el producto"}
        