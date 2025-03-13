from flask import Blueprint
from app.controllers.users.user_controller import UserController

user_bp = Blueprint("user", __name__)

user_controller = UserController()

user_bp.route("/register", methods=["GET", "POST"])(user_controller.create_user)
user_bp.route("/", methods=["GET"])(user_controller.get_users)
user_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])(user_controller.edit_user)
user_bp.route("/users/<int:user_id>/delete", methods=["DELETE"])(user_controller.delete_user)
