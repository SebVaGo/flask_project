from flask import Blueprint
from app.controllers.login_controller import AuthController

login_bp = Blueprint("auth", __name__)  
auth_controller = AuthController()

login_bp.route("/login", methods=["GET","POST"])(auth_controller.login)
