from flask import request, flash
from app.utils.forms.login_form import LoginForm
from app.controllers.auth.base_auth_controller import BaseAuthController


class AuthLoginController(BaseAuthController):
    """Maneja el inicio de sesión."""

    def login(self):
        """Maneja la solicitud de inicio de sesión."""
        form = LoginForm()

        if request.method != "POST":
            return self.render_login_form(form)

        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        return self._authenticate_user(form)

    def _authenticate_user(self, form):
        """Autentica al usuario y devuelve la respuesta."""
        resultado = self.auth_service.authenticate_user(form.correo.data, form.password.data)

        if resultado["success"]:
            return self.json_response(True, "Login exitoso", data={
                "redirect_url": self.redirect_service.get_redirect_url(resultado["user_type"])
            }, status=200)

        return self.json_response(False, resultado["message"], status=401)
