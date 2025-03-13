from flask import request
from flask_wtf.csrf import generate_csrf
from app.services.order_service import OrderService
from app.utils.forms.order_form import OrderForm, UpdateQuantityForm
from app.utils.forms.csrf_form import CSRFForm
from app.controllers.base_controller import ApiController, ViewController


order_service = OrderService()

class OrderController(ApiController, ViewController):

    def create_order(self):
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = OrderForm(data=data)
        errors = self.validate_form(form)
        if errors:
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        result = order_service.create_order(data)
        if result["success"]:
            return self.json_response(True, "Orden creada con éxito", status=201)

        return self.json_response(False, result["message"], status=400)

    def list_orders(self):
        orders = order_service.get_all_orders()
        form = CSRFForm()
        return self.render("admin/orders.html", orders=orders, form=form)

    def delete_product(self, orden_id, producto_id):
        result = order_service.delete_order_product(orden_id, producto_id)
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
        result = order_service.update_order_quantity(orden_id, producto_id, nueva_cantidad)

        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)
