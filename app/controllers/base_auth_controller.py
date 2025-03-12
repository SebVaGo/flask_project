from flask import request, jsonify
from app.utils.token_helper import TokenHelper

class BaseController:
    @staticmethod
    def get_authenticated_user():
        token = request.cookies.get("access_token")
        if not token:
            return None

        payload = TokenHelper.verify_jwt(token)
        return payload if payload else None
