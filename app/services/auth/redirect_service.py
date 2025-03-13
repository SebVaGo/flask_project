from flask import make_response, url_for


class RedirectService:

    @staticmethod
    def get_redirect_url(user_type):
        if user_type == 1:
            return url_for("admin.list_products")
        elif user_type == 2:
            return url_for("products.list")
        return url_for("home.index")