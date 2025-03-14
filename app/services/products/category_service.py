from app.services.products.base_product_service import BaseProductService

class CategoryService(BaseProductService):

    def __init__(self):
        super().__init__()

    def get_all_categories(self):
        return self.category_model.query.all()

    def get_category_by_id(self, category_id):
        return self.category_model.query.get(category_id)
    
    def validate_category(self, data):
        if "categoria_id" in data:
            categoria = self.get_category_by_id(data["categoria_id"])
            if not categoria:
                return {"success": False, "message": "Categoría no válida"}, 400
        return None, None
