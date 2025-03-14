import logging
from app.config import db
from app.services.products.base_product_service import BaseProductService
from app.services.products.category_service import CategoryService


class ProductSaveService(BaseProductService):

    def __init__(self):
        super().__init__()
        self.category_service = CategoryService()

    def save_product(self, data, product_id=None):
        session = db.session
        try:
            is_update = product_id is not None
            # 1. Validar la categoría
            error, status_code = self.category_service.validate_category(data)
            if error:
                return error, status_code
            # 2. Obtener o crear el producto
            if is_update:
                product, error, status_code = self.get_existing_product(session, product_id)
                if error:
                    return error, status_code
                self._update_product(product, data)
            else:
                product = self._create_new_product(session, data)

            session.commit()
            message = (
                "Producto actualizado exitosamente"
                if is_update
                else "Producto creado exitosamente"
            )
            code = 200 if is_update else 201
            return {"success": True, "message": message}, code

        except Exception as e:
            session.rollback()
            logging.error(f"Error al guardar el producto: {str(e)}")
            return (
                {"success": False, "message": f"Error al guardar el producto: {str(e)}"},
                500,
            )
        finally:
            session.close()

    def _update_product(self, product, data):

        for key, value in data.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)

    def _create_new_product(self, session, data):

        product = self.product_model(**data)
        session.add(product)
        session.flush() 
        return product
