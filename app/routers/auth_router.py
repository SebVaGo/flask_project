from flask import Blueprint

from app.controllers.auth.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)  

auth_controller = AuthController()

auth_bp.route("/login", methods=["GET","POST"])(auth_controller.login)
auth_bp.route("/logout", methods=["GET"])(auth_controller.logout)


