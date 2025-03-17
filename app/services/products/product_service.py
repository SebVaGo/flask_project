import logging
from app.config import db
from app.services.products.base_product_service import BaseProductService
from app.utils.db_session_manager import AltDBSessionManager
from app.services.products.product_save_service import ProductSaveService
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
            with AltDBSessionManager() as session:
                results = session.query(
                    self.product_model.id,
                    self.product_model.nombre,
                    self.product_model.precio,
                    self.category_model.nombre.label("categoria")
                ).join(self.category_model).all()
                return [self._product_to_dict(row) for row in results]
        except Exception as e:
            logging.error(f"Error in get_all_products: {str(e)}")
            return []

    def get_product_by_id(self, product_id):
        try:
            with AltDBSessionManager() as session:
                row = session.query(
                    self.product_model.id,
                    self.product_model.categoria_id,
                    self.category_model.nombre.label("categoria"),
                    self.product_model.nombre,
                    self.product_model.precio
                ).join(self.category_model).filter(self.product_model.id == product_id).first()
                if row:
                    return self._product_by_id_to_dict(row)
                return None
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

    def _product_to_dict(self, row):
        product_dict = {}
        columns = ["id", "nombre", "precio", "categoria"]
        for column in columns:
            if hasattr(row, column):
                product_dict[column] = getattr(row, column)

        return product_dict

    def _product_by_id_to_dict(self, row):
        product_dict = {}
        columns = ["id", "categoria_id", "categoria", "nombre", "precio"]
        for column in columns:
            if hasattr(row, column):
                product_dict[column] = getattr(row, column)
        return product_dict

