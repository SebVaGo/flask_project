from flask import render_template, jsonify
from app.services.auth.auth_service import AuthService
from app.services.auth.redirect_service import RedirectService


class BaseAuthController():

    def __init__(self):
        self.auth_service = AuthService()
        self.redirect_service = RedirectService()

    def render_login_form(self, form):
        return render_template("auth/login.html", form=form)
    
    def render(self, template, **context):
        return render_template(template, **context)
    
    def validate_form(self, form):
        if form.validate():
            return None
        return form.errors

    def json_response(self, success, message, data=None, errors=None, status=200):
        response = {"success": success, "message": message}
        if data:
            response["data"] = data
        if errors:
            response["errors"] = errors
        return jsonify(response), status
    
