from app.config import db
from app.models.user_model import User
from app.models.password_model import Password
from werkzeug.security import check_password_hash
from app.utils.token_helper import TokenHelper
from app.utils.cookie_helper import CookieHelper
from flask import make_response, url_for


class AuthService:

    @staticmethod
    def authenticate_user(correo, password):
        # Buscar usuario activo por correo
        user = db.session.query(User).filter_by(correo=correo, status="activo").first()
        if not user:
            return {"success": False, "message": "Credenciales incorrectas"}

        # Buscar la contraseña del usuario
        user_password = db.session.query(Password).filter_by(id_usuario=user.id).first()
        if not user_password or not check_password_hash(user_password.password_hash, password):
            return {"success": False, "message": "Credenciales incorrectas"}

        # Generar token JWT
        token = TokenHelper.generate_jwt(user.id, user.tipo_cliente_id)

        return {"success": True, "user_id": user.id, "token": token, "user_type": user.tipo_cliente_id}
    
    @staticmethod
    def create_login_response(token):
        resp = make_response({"success": True, "message": "Login exitoso"})
        CookieHelper.set_cookie(resp, "access_token", token)

        print(resp.headers)  
        return resp
    

class RedirectService:

    @staticmethod
    def get_redirect_url(user_type):
        """Devuelve la URL de redirección según el tipo de usuario"""
        if user_type == 1:
            return url_for("admin.list_products")  
        elif user_type == 2:
            return url_for("products.list")  

        return url_for("home.index")
