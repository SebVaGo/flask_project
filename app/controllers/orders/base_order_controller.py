from flask import render_template, jsonify
from app.services.orders.order_get_service import OrderQueryService
from app.services.orders.order_delete_service import OrderManagementService
from app.services.orders.order_save_service import OrderSaveService
from app.services.products.product_service import ProductService


class BaseOrderController():

    def __init__(self):
        self.order_query_service = OrderQueryService()
        self.order_management_service = OrderManagementService()
        self.order_save_service = OrderSaveService()
        self.product_query_service = ProductService()

    def render_order_form(self, order=None, form=None,  productos_disponibles=None, template="admin/order_form.html"):
        return render_template(template, order=order, form=form, productos_disponibles=productos_disponibles)

    def render_list(self, template="admin/orders.html", **context):
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