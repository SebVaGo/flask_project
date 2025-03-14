import logging
from flask import request, flash
from app.utils.forms.csrf_form import CSRFForm
from app.utils.forms.order_form import OrderForm
from app.controllers.orders.base_order_controller import BaseOrderController


class OrderCrudController(BaseOrderController):

    def __init__(self):
        super().__init__()

    def list_orders(self):
        """Muestra la lista de órdenes."""
        try:
            orders = self.order_query_service.get_all_orders()
            form = CSRFForm()
            return self.render("admin/orders.html", orders=orders, form=form)
        except Exception as e:
            logging.error(f"Error en list_orders: {str(e)}")
            flash("Ocurrió un error al obtener las órdenes.", "danger")
            return self.render("admin/orders.html", orders=[], form=CSRFForm())

    def create_order(self):
        data = request.get_json()
        if not data:
            return self.json_response(False, "No se recibieron datos JSON", status=400)

        form = OrderForm(data=data)
        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        try:
            result, status_code = self.order_save_service.save_order(data)
            return self.json_response(result["success"], result["message"], status=status_code)
        except Exception as e:
            logging.error(f"Error en create_order: {str(e)}")
            flash("Ocurrió un error al crear la orden.", "danger")
            return self.json_response(False, "Error interno del servidor", status=500)

    def edit_order(self, orden_id):
        """Muestra el formulario para editar una orden (GET) y procesa la actualización (POST)."""
        if request.method == "GET":
            try:
                order = self.order_query_service.get_order_by_id(orden_id)
                form = CSRFForm()
                productos_disponibles = self.product_query_service.get_all_products()
                return self.render(
                    "admin/edit_order.html",
                    order=order,
                    form=form,
                    productos_disponibles=productos_disponibles,
                )
            except Exception as e:
                logging.error(f"Error en GET de edit_order: {str(e)}")
                flash("Ocurrió un error al cargar la orden.", "danger")
                return self.render("admin/edit_order.html", order=None, form=CSRFForm(), productos_disponibles=[])
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
            flash("Ocurrió un error actualizando la orden", "danger")
            return self.json_response(False, "Ocurrió un error actualizando la orden", status=500)

    def delete_order(self, orden_id):
        """Elimina una orden."""
        try:
            result, status_code = self.order_management_service.delete_order_product(orden_id)
            return self.json_response(result["success"], result["message"], status=status_code)
        except Exception as e:
            logging.error(f"Error en delete_order: {str(e)}")
            return self.json_response(False, "Error interno del servidor", status=500)
