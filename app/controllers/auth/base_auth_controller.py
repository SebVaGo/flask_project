from flask import render_template
from app.controllers.base_controller import ApiController, ViewController
from app.services.auth.auth_service import AuthService
from app.services.auth.redirect_service import RedirectService


class BaseAuthController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.auth_service = AuthService()
        self.redirect_service = RedirectService()

    def render_login_form(self, form):
        """Renderiza el formulario de inicio de sesión."""
        return self.render("auth/login.html", form=form)
