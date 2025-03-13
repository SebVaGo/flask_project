from flask import Blueprint
from app.controllers.product_controller import ProductController

admin_bp = Blueprint("admin", __name__)
product_controller = ProductController()  

admin_bp.route("/products", methods=["GET"])(product_controller.list_products)

admin_bp.route("/products/new", methods=["GET"])(product_controller.new_product_form)

admin_bp.route("/products", methods=["POST"])(product_controller.create_product)

admin_bp.route('/products/<int:product_id>/delete', methods=['DELETE'])(product_controller.delete_product)

admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])(product_controller.edit_product)