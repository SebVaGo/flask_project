from flask import request, flash
from app.controllers.orders.base_order_controller import BaseOrderController
from app.utils.forms.order_form import UpdateQuantityForm, OrderForm


class OrderManageController(BaseOrderController):
    """Maneja la actualización y eliminación de órdenes."""

    def update_quantity(self, orden_id, producto_id):
        """Actualiza la cantidad de un producto en una orden."""
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = UpdateQuantityForm(data=data)
        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        nueva_cantidad = form.cantidad.data
        result = self.order_management_service.update_order_quantity(orden_id, producto_id, nueva_cantidad)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)

    def delete_product(self, orden_id, producto_id):
        """Elimina un producto específico de una orden."""
        result, status_code = self.order_management_service.delete_order_product(orden_id, producto_id)
        return self.json_response(result["success"], result["message"], status=status_code)
    
    def delete_order(self, orden_id):
        """Elimina una orden."""
        result, status_code = self.order_management_service.delete_order_product(orden_id)
        return self.json_response(result["success"], result["message"], status=status_code)
    
    def add_product(self, orden_id, producto_id):
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        data["producto_id"] = producto_id
        data["orden_id"] = orden_id
        
        form = OrderForm(data=data)
        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        cantidad = form.cantidad

        # Llamar al servicio con la cantidad validada
        result, status_code = self.order_management_service.add_product_to_order(orden_id, producto_id, cantidad)

        return self.json_response(result["success"], result["message"], status=status_code)
