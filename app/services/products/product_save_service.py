import logging
from app.config import db
from app.models.product_model import ProductModel


class ProductSaveService:

    def __init__(self, category_service):

        self.category_service = category_service

    def save_product(self, data, product_id=None):

        session = db.session
        try:
            is_update = product_id is not None

            # 1. Validar la categoría
            error, status_code = self._validate_category(data)
            if error:
                return error, status_code

            # 2. Obtener o crear el producto
            if is_update:
                product, error, status_code = self._get_existing_product(session, product_id)
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

    def _validate_category(self, data):
        if "categoria_id" in data:
            categoria = self.category_service.get_category_by_id(data["categoria_id"])
            if not categoria:
                return {"success": False, "message": "Categoría no válida"}, 400
        return None, None

    def _get_existing_product(self, session, product_id):

        product = session.query(ProductModel).get(product_id)
        if not product:
            return None, {"success": False, "message": "Producto no encontrado"}, 404
        return product, None, None

    def _update_product(self, product, data):

        for key, value in data.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)

    def _create_new_product(self, session, data):

        product = ProductModel(**data)
        session.add(product)
        session.flush() 
        return product
