from flask import request, jsonify, render_template

    
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