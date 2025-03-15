from flask import render_template, jsonify
from app.services.products.product_service import ProductService
from app.services.products.category_service import CategoryService


class BaseProductController():

    def __init__(self):
        self.product_service = ProductService()
        self.category_service = CategoryService()

    def render_product_form(self, form, template="admin/product_form.html", product=None):
        return render_template(template, form=form, product=product)
    
    def render_list(self, template="admin/products.html", **context):
        return render_template(template, **context)
    
    def validate_form(self, form):
        if form.validate():
            return None
        return form.errors

    def json_response(self, success, message, data=None, errors=None, status=200):
        response = {"success": success, "message": message}
        if data:
            response["data"] = data
        if errors:
            response["errors"] = errors
        return jsonify(response), status
    

