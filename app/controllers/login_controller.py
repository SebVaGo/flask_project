from flask import request, jsonify, make_response, render_template, redirect, url_for
from app.utils.forms.login_form import LoginForm
from app.controllers.base_auth_controller import BaseController

from app.services.auth_service import AuthService, RedirectService

class AuthController(BaseController):
    @staticmethod
    def login():
        form = LoginForm()

        if request.method == "POST":
            if form.validate_on_submit():
                correo = form.correo.data
                password = form.password.data
                resultado = AuthService.authenticate_user(correo, password)

                if resultado["success"]:
                    response = AuthService.create_login_response(resultado["token"])
                    return jsonify({"success": True, "redirect_url": RedirectService.get_redirect_url(resultado["user_type"])}), 200

                return jsonify({"success": False, "message": resultado["message"]}), 401

            return jsonify({"success": False, "errors": form.errors}), 400

        return render_template("login.html", form=form)