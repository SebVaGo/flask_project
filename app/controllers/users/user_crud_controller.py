import logging
from flask import request, flash
from app.utils.forms.user_form import UserForm, UserUpdateForm
from app.utils.forms.csrf_form import CSRFForm
from app.controllers.users.base_user_controller import BaseUserController


class UserCrudController(BaseUserController):

    def __init__(self):
        super().__init__()

    def get_users(self):
        try:
            users = self.user_service.get_all_users()
            form = CSRFForm()
            return self.render_list(users=users, form=form)
        except Exception as e:
            logging.error(f"Error in get_users: {str(e)}")
            flash("Ocurrió un error al obtener los usuarios.", "danger")
            return self.render_list(users=[], form=CSRFForm())

    def create_user(self):
        try:
            form = UserForm()
            form.tipo_cliente_id.choices = self.get_client_types()

            if request.method == "GET":
                return self.render_user_form(form)

            errors = self.validate_form(form)
            if errors:
                return self.json_response(False, "Errores de validación", errors=errors, status=400)

            data = {
                key: value
                for key, value in form.data.items()
                if key not in ["submit", "csrf_token"]
            }
            resultado, status_code = self.user_service.save_user(data)

            if resultado["success"]:
                flash("Usuario creado correctamente.", "success")
                return self.json_response(True, "Usuario creado correctamente.", status=status_code)

            flash(resultado["message"], "danger")
            return self.json_response(False, resultado["message"], status=status_code)

        except Exception as e:
            logging.error(f"Error in create_user: {str(e)}")
            flash("Ocurrió un error al crear el usuario.", "danger")
            return self.json_response(False, "Error interno del servidor", status=500)
    
    def edit_user(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            if not user:
                return self.json_response(False, "Usuario no encontrado.", status=404)

            form = UserUpdateForm(obj=user)
            form.tipo_cliente_id.choices = self.get_client_types()

            if request.method == "GET":
                return self.render_user_form(form, user=user)

            errors = self.validate_form(form)
            if errors:
                return self.json_response(False, "Errores de validación", errors=errors, status=400)

            data = {
                key: value
                for key, value in form.data.items()
                if key not in ["submit", "csrf_token"]
            }
            resultado, status_code = self.user_service.save_user(data, user_id)
            return self.json_response(resultado["success"], resultado["message"], status=status_code)

        except Exception as e:
            logging.error(f"Error in edit_user: {str(e)}")
            flash("Ocurrió un error al editar el usuario.", "danger")
            return self.json_response(False, "Error interno del servidor", status=500)

    def delete_user(self, user_id):
        try:
            resultado = self.user_service.delete_user(user_id)
            return self.json_response(
                resultado["success"],
                resultado["message"],
                status=200 if resultado["success"] else 400
            )
        except Exception as e:
            logging.error(f"Error in delete_user: {str(e)}")
            return self.json_response(False, "Error interno del servidor", status=500)
