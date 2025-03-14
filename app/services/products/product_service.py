from app.config import db
from app.models.product_model import ProductModel
from app.services.products.category_service import CategoryService
from app.services.products.order_cleanup_service import OrderCleanupService
from app.services.products.product_save_service import ProductSaveService
from app.utils.db_session_manager import DBSessionManager
from sqlalchemy import update


class ProductService:

    def __init__(self):
        self.db_manager = DBSessionManager()
        self.category_service = CategoryService()
        self.order_cleanup_service = OrderCleanupService()
        self.product_save_service = ProductSaveService(self.category_service)
        self.product_model = ProductModel

    def save_product(self, data, product_id=None):
        return self.product_save_service.save_product(data, product_id)

    def get_all_products(self):
        return db.session.query(
            self.product_model.id,
            self.product_model.nombre,
            self.product_model.precio,
            self.category_service.category_model.nombre.label("categoria")
        ).join(self.category_service.category_model).all()

    def get_product_by_id(self, product_id):
        return db.session.query(
            self.product_model.id,
            self.product_model.categoria_id,
            self.category_service.category_model.nombre.label("categoria"),
            self.product_model.nombre,
            self.product_model.precio
        ).join(self.category_service.category_model).filter(self.product_model.id == product_id).first()

    def delete_product(self, product_id):
        product = self.product_model.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}

        try:
            self.order_cleanup_service.delete_orders_by_product(product_id)
            db.session.delete(product)
            self.db_manager.commit()
            return {"success": True, "message": "Producto eliminado correctamente"}
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar el producto: {str(e)}"}
