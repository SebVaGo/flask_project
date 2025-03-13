from flask import request, flash
from app.controllers.orders.base_order_controller import BaseOrderController
from app.utils.forms.order_form import OrderForm


class OrderCreateController(BaseOrderController):
    """Maneja la creación de órdenes."""

    def create_order(self):
        """Crea una nueva orden."""
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = OrderForm(data=data)
        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        result = self.order_creation_service.create_order(data)
        return self.json_response(result["success"], result["message"], status=201 if result["success"] else 400)
