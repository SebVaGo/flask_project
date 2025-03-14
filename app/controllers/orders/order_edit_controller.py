import logging

from flask import request, flash
from app.controllers.orders.base_order_controller import BaseOrderController
from app.utils.forms.order_form import OrderForm

class OrderUpdateController(BaseOrderController):

    def update_order(self, orden_id):
            try:
                data = request.get_json()
                if not data:
                    message = "No se recibieron datos JSON"
                    flash(message, "danger")
                    return self.json_response(False, message, status=400)

                form = OrderForm(data=data)
                errors = self.validate_form(form)
                if errors:
                    flash("Errores de validación", "danger")
                    return self.json_response(False, "Errores de validación", errors=errors, status=400)

                result, status_code = self.order_save_service.save_order(data, order_id=orden_id)

                if not result["success"]:
                    flash(result["message"], "danger")
                else:
                    flash(result["message"], "success")

                return self.json_response(result["success"], result["message"], status=status_code)

            except Exception as e:
                logging.error(f"Error en update_order: {str(e)}")
                flash("Ocurrió un error actualizando la ordern", "danger")
                return self.json_response(False, "Ocurrió un error actualizando la orden", status=500)