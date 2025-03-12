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
