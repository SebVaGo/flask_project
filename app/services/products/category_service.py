from app.models.categoy_product_model import CategoryModel


class CategoryService:

    def __init__(self):
        self.category_model = CategoryModel

    def get_all_categories(self):
        return self.category_model.query.all()

    def get_category_by_id(self, category_id):
        return self.category_model.query.get(category_id)
