from flask import request, flash, render_template

from app.services.users.user_service import UserService, ClientTypeService
from app.utils.forms.user_form import UserForm, UserUpdateForm
from app.utils.forms.csrf_form import CSRFForm
from app.controllers.base_controller import ApiController, ViewController


class UserController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.client_type_service = ClientTypeService()

    def create_user(self):
        form = UserForm()
        client_types = self.client_type_service.get_all_types()
        form.tipo_cliente_id.choices = [(tipo.id, tipo.nombre) for tipo in client_types]

        if request.method == "POST" and form.validate_on_submit():
            data = {
                key: value for key, value in form.data.items() 
                if key not in ["submit", "csrf_token"]
            }
            resultado = self.user_service.create_user(data)

            if resultado["success"]:
                flash("Usuario creado correctamente.", "success")
                return self.json_response(True, "Usuario creado correctamente.", status=201)

            flash(resultado["message"], "danger")
            return self.json_response(False, resultado["message"], status=400)

        if request.method == "POST":
            return self.json_response(False, "Errores de validación", errors=form.errors, status=400)

        return self.render("register.html", form=form)

    def get_users(self):
        users = self.user_service.get_all_users()
        form = CSRFForm()
        return self.render("users.html", users=users, form=form)

    def edit_user(self, user_id):
        user = self.user_service.get_user_by_id(user_id)
        
        if not user:
            return self.json_response(False, "Usuario no encontrado.", status=404)

        form = UserUpdateForm(obj=user)
        client_types = self.client_type_service.get_all_types()
        form.tipo_cliente_id.choices = [(tipo.id, tipo.nombre) for tipo in client_types]

        if request.method == "POST" and form.validate_on_submit():
            data = {
                key: value for key, value in form.data.items()
                if key not in ["submit", "csrf_token"]
            }
            resultado, status_code = self.user_service.update_user(user_id, data)
            return self.json_response(resultado["success"], resultado["message"], status=status_code)

        if request.method == "POST":
            return self.json_response(False, "Errores de validación", errors=form.errors, status=400)

        return self.render("edit_user.html", user=user, form=form)

    def delete_user(self, user_id):
        resultado = self.user_service.delete_user(user_id)
        return self.json_response(resultado["success"], resultado["message"], status=200 if resultado["success"] else 400)