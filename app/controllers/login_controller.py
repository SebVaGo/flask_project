from flask import request, jsonify, make_response, render_template
from app.utils.forms.login_form import LoginForm

from app.services.auth_service import AuthService

class AuthController:
    @staticmethod
    def login():
        form = LoginForm()

        if request.method == "POST":
            if form.validate_on_submit():
                correo = form.correo.data
                password = form.password.data
                resultado = AuthService.authenticate_user(correo, password)

                if resultado["success"]:
                    return jsonify({"success": True, "message": "Login exitoso"}), 200

                return jsonify({"success": False, "message": resultado["message"]}), 401

            return jsonify({"success": False, "errors": form.errors}), 400

        return render_template("login.html", form=form)