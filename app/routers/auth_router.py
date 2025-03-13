from flask import Blueprint
from app.controllers.auth.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)  

auth_controller = AuthController()

auth_bp.route("/login", methods=["GET","POST"])(auth_controller.login)
