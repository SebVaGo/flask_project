from flask import Blueprint, render_template
from app.controllers.user_controller import create_user, get_users, edit_user, delete_user

user_bp = Blueprint("user", __name__)

user_bp.route("/register", methods=["GET", "POST"])(create_user)
user_bp.route("/", methods=["GET"])(get_users)
user_bp.route("/users/<int:user_id>/edit", methods=["GET", "POST"])(edit_user)
user_bp.route("/users/<int:user_id>/delete", methods=["DELETE"])(delete_user)


@user_bp.route("/success")
def success_page():
    return render_template("success_page.html")
