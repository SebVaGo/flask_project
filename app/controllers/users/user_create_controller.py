from flask import request, flash
from app.controllers.users.base_user_controller import BaseUserController
from app.utils.forms.user_form import UserForm


class UserCreateController(BaseUserController):

    def create_user(self):
        form = UserForm()
        form.tipo_cliente_id.choices = self.get_client_types()

        if request.method == "POST":
            errors = self.validate_form(form)
            if errors:
                flash("Errores de validación", "danger")
                return self.json_response(False, "Errores de validación", errors=errors, status=400)

            data = {key: value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}
            resultado = self.user_service.create_user(data)

            if resultado["success"]:
                flash("Usuario creado correctamente.", "success")
                return self.json_response(True, "Usuario creado correctamente.", status=201)

            flash(resultado["message"], "danger")
            return self.json_response(False, resultado["message"], status=400)

        return self.render_user_form(form)
