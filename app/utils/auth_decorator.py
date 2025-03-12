from functools import wraps
from flask import jsonify
from app.controllers.base_auth_controller import BaseController

def require_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user = BaseController.get_authenticated_user()
        if not user:
            return jsonify({"success": False, "message": "No autorizado"}), 401
        return func(*args, **kwargs)
    return wrapper
