from flask import request, make_response

class CookieHelper:
    """Clase para manejar la creación, verificación y eliminación de cookies"""

    @staticmethod
    def set_cookie(response, key, value, expires=None):
        """Asigna una cookie segura a la respuesta"""
        response.set_cookie(
            key,
            value,
            httponly=True,
            secure=True,
            samesite="Strict",
            max_age=expires
        )

    @staticmethod
    def get_cookie(key):
        """Obtiene el valor de una cookie desde la solicitud"""
        return request.cookies.get(key)

    @staticmethod
    def delete_cookie(response, key):
        """Elimina una cookie asignándola como vacía y expirando su tiempo"""
        response.set_cookie(
            key,
            "",
            expires=0,
            httponly=True,
            secure=True,
            samesite="Strict"
        )
