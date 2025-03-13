from flask import Blueprint
from app.controllers.order_controller import OrderController

order_bp = Blueprint("order", __name__)
order_controller = OrderController()

order_bp.route("/orders", methods=["POST"])(order_controller.create_order)
order_bp.route("/orders", methods=["GET"])(order_controller.list_orders)
order_bp.route("/orders/<int:orden_id>/<int:producto_id>/delete", methods=["DELETE"])(order_controller.delete_product)
order_bp.route('/orders/<int:orden_id>/<int:producto_id>/update', methods=['PUT'])(order_controller.update_quantity)
