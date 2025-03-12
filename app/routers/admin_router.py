from flask import Blueprint
from app.controllers.product_controller import ProductController

admin_bp = Blueprint("admin", __name__)

# Ruta para listar productos
admin_bp.route("/products", methods=["GET"])(ProductController.list_products)

# Ruta para mostrar el formulario de creación
admin_bp.route("/products/new", methods=["GET"])(ProductController.new_product_form)

# Ruta para crear un producto (POST)
admin_bp.route("/products", methods=["POST"])(ProductController.create_product)

admin_bp.route("/products/<int:product_id>/delete", methods=["DELETE"])(ProductController.delete_product)
