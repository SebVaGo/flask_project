import jwt
import datetime
from app.config import Config  

class TokenHelper:

    @staticmethod
    def generate_jwt(user_id, user_type):
        payload = {
            "user_id": user_id,
            "user_type_id": user_type,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2),
            "iat": datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
        return token

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None  
        except jwt.InvalidTokenError:
            return None  
