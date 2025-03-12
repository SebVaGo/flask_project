from app.models.user_model import User
from app.models.password_model import Password
from werkzeug.security import check_password_hash
from app.utils.token_helper import TokenHelper
from app.utils.cookie_helper import CookieHelper
from flask import make_response, url_for


class AuthService:

    @staticmethod
    def authenticate_user(correo, password):

        user = User.query.filter_by(correo=correo, status="activo").first()
        if not user:
            return {"success": False, "message": "Credenciales incorrectas"}

        user_password = Password.query.filter_by(id_usuario=user.id).first()
        if not user_password or not check_password_hash(user_password.password_hash, password):
            return {"success": False, "message": "Credenciales incorrectas"}

        token = TokenHelper.generate_jwt(user.id, user.tipo_cliente_id)

        return {"success": True, "user_id": user.id, "token": token, "user_type": user.tipo_cliente_id}

    @staticmethod
    def create_login_response(token):
        resp = make_response({"success": True, "message": "Login exitoso"})
        CookieHelper.set_cookie(resp, "access_token", token)
        return resp

class RedirectService:

    @staticmethod
    def get_redirect_url(user_type):
        """Devuelve la URL de redirección según el tipo de usuario"""
        if user_type == 1:
            return "/admin/dashboard"  # Simulación de ruta de administrador
        
        elif user_type == 2:
            return "/products"  # Simulación de ruta de productos
        
        return "/"