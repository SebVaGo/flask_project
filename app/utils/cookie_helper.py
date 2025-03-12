from flask import request, make_response

class CookieHelper:

    @staticmethod
    def set_cookie(response, key, value, expires=None):
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
        return request.cookies.get(key)

    @staticmethod
    def delete_cookie(response, key):
        response.set_cookie(
            key,
            "",
            expires=0,
            httponly=True,
            secure=True,
            samesite="Strict"
        )
