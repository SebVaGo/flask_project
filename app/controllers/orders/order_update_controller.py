from flask import request, flash
from app.controllers.orders.base_order_controller import BaseOrderController
from app.utils.forms.order_form import OrderForm

class OrderUpdateController(BaseOrderController):

    def update_order(self, orden_id):
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = OrderForm(data=data)
        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        result, status_code = self.order_save_service.save_order(data, order_id=orden_id)
        return self.json_response(result["success"], result["message"], status=status_code)
