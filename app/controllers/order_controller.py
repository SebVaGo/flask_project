from flask import request, jsonify
from flask_wtf.csrf import generate_csrf
from app.services.order_service import OrderService
from app.utils.forms.order_form import OrderForm, UpdateQuantityForm
from app.controllers.base_controller import BaseController

order_service = OrderService()

class OrderController(BaseController):

    def __init__(self):
        super().__init__() 

    def create_order(self):
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No se recibieron datos JSON"}), 400

        form = OrderForm(data=data)

        errors = self.validate_form(form, json=True)
        if errors:
            return jsonify({"success": False, "message": "Errores de validación", "errors": errors}), 400

        result = order_service.create_order(data)

        if result["success"]:
            return jsonify({"success": True, "message": "Orden creada con éxito"}), 201

        return jsonify({"success": False, "message": result["message"]}), 400

    def list_orders(self):
        orders = order_service.get_all_orders()
        csrf_token = generate_csrf()
        return self.render("admin/orders.html", orders=orders, csrf_token=csrf_token)

    def delete_product(self, orden_id, producto_id):
        result = order_service.delete_order_product(orden_id, producto_id)

        if result["success"]:
            return jsonify({"success": True, "message": "Producto eliminado"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400

    def update_quantity(self, orden_id, producto_id):
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No se recibieron datos JSON"}), 400

        form = UpdateQuantityForm(data=data)

        errors = self.validate_form(form, json=True)
        if errors:
            return jsonify({"success": False, "message": "Errores de validación", "errors": errors}), 400

        nueva_cantidad = form.cantidad.data

        result = order_service.update_order_quantity(orden_id, producto_id, nueva_cantidad)

        if result["success"]:
            return jsonify({"success": True, "message": "Cantidad actualizada"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400
