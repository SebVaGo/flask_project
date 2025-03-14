from flask import request, flash
from app.controllers.users.base_user_controller import BaseUserController
from app.utils.forms.user_form import UserUpdateForm


class UserEditController(BaseUserController):

    def edit_user(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        if not user:
            return self.json_response(False, "Usuario no encontrado.", status=404)

        form = UserUpdateForm(obj=user)
        form.tipo_cliente_id.choices = self.get_client_types()

        if request.method == "POST":
            errors = self.validate_form(form)
            if errors:
                flash("Errores de validación", "danger")
                return self.json_response(False, "Errores de validación", errors=errors, status=400)

            data = {key: value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}
            resultado, status_code = self.user_service.save_user(data, user_id)
            
            return self.json_response(resultado["success"], resultado["message"], status=status_code)

        return self.render_user_form(form, template="edit_user.html", user=user)
