from flask import render_template
from app.controllers.base_controller import ApiController, ViewController
from app.services.products.product_service import ProductService
from app.services.products.category_service import CategoryService


class BaseProductController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.product_service = ProductService()
        self.category_service = CategoryService()

    def render_product_form(self, form, template="admin/product_form.html", product=None):
        return self.render(template, form=form, product=product)
