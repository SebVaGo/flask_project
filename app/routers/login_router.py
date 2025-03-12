from flask import Blueprint
from app.controllers.login_controller import AuthController

login_bp = Blueprint("auth", __name__)  # Nombre del Blueprint

# Ruta para iniciar sesión
login_bp.route("/login", methods=["GET","POST"])(AuthController.login)
