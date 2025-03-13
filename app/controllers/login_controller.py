from flask import request
from app.utils.forms.login_form import LoginForm
from app.controllers.base_controller import ApiController, ViewController 
from app.services.auth_service import AuthService, RedirectService

class AuthController(ApiController, ViewController):
    
    def login(self):
        form = LoginForm()

        if request.method == "POST":
            if form.validate_on_submit():
                correo = form.correo.data
                password = form.password.data
                resultado = AuthService.authenticate_user(correo, password)

                if resultado["success"]:
                    return self.json_response(True, "Login exitoso", data={
                        "redirect_url": RedirectService.get_redirect_url(resultado["user_type"])
                    }, status=200)

                return self.json_response(False, resultado["message"], status=401)

            return self.json_response(False, "Errores de validación", errors=form.errors, status=400)

        return self.render("auth/login.html", form=form) 
