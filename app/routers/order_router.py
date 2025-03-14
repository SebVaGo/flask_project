from flask import Blueprint
from app.controllers.orders.order_controller import OrderController

order_bp = Blueprint("order", __name__)
order_controller = OrderController()

order_bp.route("/orders", methods=["GET"])(order_controller.list_orders)
order_bp.route("/orders", methods=["POST"])(order_controller.create_order)
order_bp.route("/orders/<int:orden_id>/edit", methods=["GET", "PUT"])(order_controller.edit_order)
order_bp.route("/orders/<int:orden_id>/delete", methods=["DELETE"])(order_controller.delete_order)



