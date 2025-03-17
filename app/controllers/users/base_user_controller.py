from flask import jsonify, render_template
from app.services.users.user_service import UserService
from app.services.users.client_type_service import ClientTypeService


class BaseUserController():

    def __init__(self):
        self.user_service = UserService()
        self.client_type_service = ClientTypeService()

    def render_user_form(self, form, template="user_form.html", user=None):
        return render_template(template, form=form, user=user)

    def render_list(self, template="users.html", **context):
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