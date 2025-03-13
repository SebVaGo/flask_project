from flask import request, jsonify, render_template


class BaseController:

    def validate_form(self, form, json=False):
        if json:
            if form.validate():
                return None
        else:
            if form.validate_on_submit():
                return None
        return form.errors

    def render(self, template, **context):
        return render_template(template, **context)
    
class ApiController:
    
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


class ViewController:
    
    def render(self, template, **context):
        return render_template(template, **context)