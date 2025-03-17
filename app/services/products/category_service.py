import logging
from app.services.products.base_product_service import BaseProductService
from app.utils.db_session_manager import AltDBSessionManager

class CategoryService(BaseProductService):

    def __init__(self):
        super().__init__()

    def get_all_categories(self):
        try:
            with AltDBSessionManager() as session:
                categories = session.query(self.category_model).all()
                cat_list = [{"id": cat.id, "nombre": cat.nombre} for cat in categories]
                return cat_list
        except Exception as e:
            logging.error(f"Error in get_all_categories: {str(e)}")
            return []

    def get_category_by_id(self, category_id):
        try:
            with AltDBSessionManager() as session:
                cat = session.query(self.category_model).get(category_id)
                if cat:
                    return {"id": cat.id, "nombre": cat.nombre}
                return None
        except Exception as e:
            logging.error(f"Error in get_category_by_id: {str(e)}")
            return None

    def validate_category(self, data, session=None):
        try:
            if "categoria_id" in data:
                if session:
                    cat = session.query(self.category_model).get(data["categoria_id"])
                else:
                    cat = self.category_model.query.get(data["categoria_id"])
                if not cat:
                    return {"success": False, "message": "Categoría no válida"}, 400
            return None, None
        except Exception as e:
            logging.error(f"Error in validate_category: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500
