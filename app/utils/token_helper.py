import jwt
import datetime
from app.config import Config  

class TokenHelper:
    """Clase para manejar la generación y validación de tokens JWT"""

    @staticmethod
    def generate_jwt(user_id):
        """Genera un token JWT con el ID del usuario"""
        payload = {
            "user_id": user_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_jwt(token):
        """Verifica un token JWT y devuelve los datos decodificados o None si es inválido"""
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
