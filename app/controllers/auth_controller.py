from flask import request

from app.utils.forms.login_form import LoginForm
from app.controllers.base_controller import ApiController, ViewController
from app.services.auth.auth_service import AuthService
from app.services.auth.redirect_service import RedirectService


class AuthController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.redirect_service = RedirectService()

    def login(self):
        form = LoginForm()

        if request.method != "POST":
            return self.render_login_form(form)

        if not form.validate_on_submit():
            return self.json_response(False, "Errores de validación", errors=form.errors, status=400)

        return self._authenticate_user(form)

    def _authenticate_user(self, form):
        resultado = self.auth_service.authenticate_user(form.correo.data, form.password.data)

        if resultado["success"]:
            return self.json_response(True, "Login exitoso", data={
                "redirect_url": self.redirect_service.get_redirect_url(resultado["user_type"])
            }, status=200)

        return self.json_response(False, resultado["message"], status=401)

    def render_login_form(self, form):
        return self.render("auth/login.html", form=form)
