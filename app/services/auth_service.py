from app.models.user_model import User
from app.models.password_model import Password
from werkzeug.security import check_password_hash
from app.utils.token_helper import TokenHelper
from app.utils.cookie_helper import CookieHelper
from flask import make_response


class AuthService:
    """Clase encargada de la autenticación y generación de tokens JWT"""

    @staticmethod
    def authenticate_user(correo, password):
        """Verifica credenciales y genera un token si son correctas"""

        user = User.query.filter_by(correo=correo, status="activo").first()
        if not user:
            return {"success": False, "message": "Credenciales incorrectas"}

        user_password = Password.query.filter_by(id_usuario=user.id).first()
        if not user_password or not check_password_hash(user_password.password_hash, password):
            return {"success": False, "message": "Credenciales incorrectas"}

        token = TokenHelper.generate_jwt(user.id)

        return {"success": True, "user_id": user.id, "token": token}

    @staticmethod
    def create_login_response(token):
        """Crea la respuesta HTTP y asigna la cookie usando CookieHelper"""
        resp = make_response({"success": True, "message": "Login exitoso"})
        CookieHelper.set_cookie(resp, "access_token", token)
        return resp
