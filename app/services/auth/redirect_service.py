from flask import url_for


class RedirectService:
    """Maneja las redirecciones después del login."""

    @staticmethod
    def get_redirect_url(user_type):
        """Devuelve la URL de redirección según el tipo de usuario."""
        if user_type == 1:
            return url_for("admin.list_products")  # ✅ Ahora coincide con el blueprint `admin`
        elif user_type == 2:
            return url_for("admin.list_products")  # ✅ También para clientes, si aplica

        return url_for("home.index")
