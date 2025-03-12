from app.models.user_model import User
from app.models.password_model import Password
from werkzeug.security import check_password_hash
from app.utils.token_helper import TokenHelper

class AuthService:
    """Clase encargada de la autenticación y generación de tokens JWT"""

    @staticmethod
    def authenticate_user(correo, password):
        """Verifica credenciales y genera un token si son correctas"""

        # Buscar usuario por correo
        user = User.query.filter_by(correo=correo, status="activo").first()
        if not user:
            return {"success": False, "message": "Credenciales incorrectas"}

        # Buscar la contraseña del usuario en la tabla `passwords`
        user_password = Password.query.filter_by(id_usuario=user.id).first()
        if not user_password or not check_password_hash(user_password.password_hash, password):
            return {"success": False, "message": "Credenciales incorrectas"}

        # Generar token JWT
        token = TokenHelper.generate_jwt(user.id)

        return {"success": True, "user_id": user.id, "token": token}
