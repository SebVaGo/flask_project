from flask import request, jsonify, render_template, redirect, url_for
from flask_wtf.csrf import generate_csrf

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