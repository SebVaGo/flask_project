import logging
from app.services.products.base_product_service import BaseProductService


class CategoryService(BaseProductService):

    def __init__(self):
        super().__init__()

    def get_all_categories(self):
        try:
            return self.category_model.query.all()
        except Exception as e:
            logging.error(f"Error in get_all_categories: {str(e)}")
            return []

    def get_category_by_id(self, category_id):
        try:
            return self.category_model.query.get(category_id)
        except Exception as e:
            logging.error(f"Error in get_category_by_id: {str(e)}")
            return None

    def validate_category(self, data):
        try:
            if "categoria_id" in data:
                categoria = self.get_category_by_id(data["categoria_id"])
                if not categoria:
                    return {"success": False, "message": "Categoría no válida"}, 400
            return None, None
        except Exception as e:
            logging.error(f"Error in validate_category: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500
