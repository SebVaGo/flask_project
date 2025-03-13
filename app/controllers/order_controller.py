from flask import request, flash, render_template

from app.services.orders.order_creation_service import OrderCreationService
from app.services.orders.order_query_service import OrderQueryService
from app.services.orders.order_manage_service import OrderManagementService
from app.utils.forms.order_form import OrderForm, UpdateQuantityForm
from app.utils.forms.csrf_form import CSRFForm
from app.controllers.base_controller import ApiController, ViewController


class OrderController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.order_creation_service = OrderCreationService()
        self.order_query_service = OrderQueryService()
        self.order_management_service = OrderManagementService()

    def create_order(self):
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = OrderForm(data=data)
        errors = self.validate_form(form)
        if errors:
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        result = self.order_creation_service.create_order(data)
        return self.json_response(result["success"], result["message"], status=201 if result["success"] else 400)

    def list_orders(self):
        orders = self.order_query_service.get_all_orders()
        form = CSRFForm()
        return self.render("admin/orders.html", orders=orders, form=form)

    def delete_product(self, orden_id, producto_id):
        result = self.order_management_service.delete_order_product(orden_id, producto_id)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)

    def update_quantity(self, orden_id, producto_id):
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = UpdateQuantityForm(data=data)
        errors = self.validate_form(form)
        if errors:
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        nueva_cantidad = form.cantidad.data
        result = self.order_management_service.update_order_quantity(orden_id, producto_id, nueva_cantidad)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)