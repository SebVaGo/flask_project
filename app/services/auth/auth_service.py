from flask import make_response, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

from app.models.user_model import UserModel
from app.models.password_model import PasswordModel
from app.utils.db_session_manager import DBSessionManager

class AuthService:
    def __init__(self):
        self.db_manager = DBSessionManager()
        self.user_model = UserModel
        self.password_model = PasswordModel

    def authenticate_user(self, correo, password):
        user = self.user_model.query.filter_by(correo=correo, status="activo").first()
        if not user:
            return {"success": False, "message": "Credenciales incorrectas"}

        user_password = self.password_model.query.filter_by(id_usuario=user.id).first()
        if not user_password or not check_password_hash(user_password.password_hash, password):
            return {"success": False, "message": "Credenciales incorrectas"}
        
        login_user(user)
        
        return {
            "success": True, 
            "user_id": user.id,
            "user_type": user.tipo_cliente_id
        }
    
    def logout(self):
        logout_user()
        return {"success": True, "message": "Sesión cerrada"}