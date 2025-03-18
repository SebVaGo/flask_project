from app.controllers.products.product_crud_controller import ProductCrudController
from app.utils.decorators import admin_and_login_required_for_all_methods


@admin_and_login_required_for_all_methods
class ProductController(ProductCrudController):
    pass
