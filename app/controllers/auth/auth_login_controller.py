from flask import request, flash
from app.utils.forms.login_form import LoginForm
from app.controllers.auth.base_auth_controller import BaseAuthController

class AuthLoginController(BaseAuthController):
    """Maneja el inicio de sesión."""

    def login(self):
        if request.method == "GET":
            try:
                form = LoginForm()
                return self.render_login_form(form)
            except Exception as e:
                flash("Error al cargar el formulario de inicio de sesión.", "danger")
                return self.json_response(False, "Error interno del servidor", status=500)
        else:
            try:
                form = LoginForm(request.form)
                errors = self.validate_form(form)
                if errors:
                    flash("Errores de validación", "danger")
                    return self.json_response(False, "Errores de validación", errors=errors, status=400)

                return self._authenticate_user(form)
            except Exception as e:
                flash("Ocurrió un error al procesar el inicio de sesión.", "danger")
                return self.json_response(False, "Error interno del servidor", status=500)

    def _authenticate_user(self, form):
        resultado = self.auth_service.authenticate_user(form.correo.data, form.password.data)

        if resultado["success"]:
            return self.json_response(True, "Login exitoso", data={
                "redirect_url": self.redirect_service.get_redirect_url(resultado["user_type"])
            }, status=200)

        return self.json_response(False, resultado["message"], status=401)
