import logging
from app.config import db
from app.services.products.product_save_service import ProductSaveService
from app.services.products.base_product_service import BaseProductService
from sqlalchemy import update


class ProductService(BaseProductService):

    def __init__(self):
        super().__init__()
        self.product_save_service = ProductSaveService()

    def save_product(self, data, product_id=None):
        try:
            return self.product_save_service.save_product(data, product_id)
        except Exception as e:
            logging.error(f"Error in save_product: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500

    def get_all_products(self):
        try:
            products = db.session.query(
                self.product_model.id,
                self.product_model.nombre,
                self.product_model.precio,
                self.category_model.nombre.label("categoria")
            ).join(self.category_model).all()
            return products
        except Exception as e:
            logging.error(f"Error in get_all_products: {str(e)}")
            return []

    def get_product_by_id(self, product_id):
        try:
            product = db.session.query(
                self.product_model.id,
                self.product_model.categoria_id,
                self.category_model.nombre.label("categoria"),
                self.product_model.nombre,
                self.product_model.precio
            ).join(self.category_model).filter(self.product_model.id == product_id).first()
            return product
        except Exception as e:
            logging.error(f"Error in get_product_by_id: {str(e)}")
            return None

    def delete_product(self, product_id):
        product = self.product_model.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}

        try:
            self.delete_orders_by_product(product_id)
            db.session.delete(product)
            self.db_manager.commit()
            return {"success": True, "message": "Producto eliminado correctamente"}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error in delete_product: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}

    def delete_orders_by_product(self, product_id):
        try:
            db.session.query(self.order_model).filter_by(producto_id=product_id).delete()
        except Exception as e:
            logging.error(f"Error in delete_orders_by_product: {str(e)}")
