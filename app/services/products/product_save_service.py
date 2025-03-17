import logging
from app.services.products.base_product_service import BaseProductService
from app.services.products.category_service import CategoryService
from app.utils.db_session_manager import AltDBSessionManager

class ProductSaveService(BaseProductService):

    def __init__(self):
        super().__init__()
        self.category_service = CategoryService()

    def save_product(self, data, product_id=None):
        try:
            with AltDBSessionManager() as session:
                is_update = product_id is not None
                error, status_code = self.category_service.validate_category(data, session)
                if error:
                    return error, status_code
                if is_update:
                    product, error, status_code = self.get_existing_product(session, product_id)
                    if error:
                        return error, status_code
                    self._update_product(session, product, data)
                else:
                    product = self._create_new_product(session, data)
                message = "Producto actualizado exitosamente" if is_update else "Producto creado exitosamente"
                code = 200 if is_update else 201
                return {"success": True, "message": message}, code
        except Exception as e:
            session.rollback()
            logging.error(f"Error al guardar el producto: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500
        finally:
            session.close()

    def get_existing_product(self, session, product_id):
        try:
            product = session.query(self.product_model).get(product_id)
            if not product:
                return None, {"success": False, "message": "Producto no encontrado"}, 404
            return product, None, None
        except Exception as e:
            logging.error(f"Error in get_existing_product: {str(e)}")
            return None, {"success": False, "message": "Error interno del servidor"}, 500

    def _update_product(self, session, product, data):
        for key, value in data.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)

    def _create_new_product(self, session, data):
        try:
            product = self.product_model(**data)
            session.add(product)
            session.flush()
            return product
        except Exception as e:
            logging.error(f"Error in _create_new_product: {str(e)}")
            raise Exception("Error al crear un nuevo producto.")
