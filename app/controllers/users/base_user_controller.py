from flask import request, flash, render_template
from app.controllers.base_controller import ApiController, ViewController
from app.utils.forms.csrf_form import CSRFForm
from app.utils.forms.user_form import UserForm, UserUpdateForm
from app.services.users.user_service import UserService, ClientTypeService


class BaseUserController(ApiController, ViewController):

    def __init__(self):
        super().__init__()
        self.user_service = UserService()
        self.client_type_service = ClientTypeService()

    def get_client_types(self):
        client_types = self.client_type_service.get_all_types()
        return [(tipo.id, tipo.nombre) for tipo in client_types]

    def render_user_form(self, form, template="user_form.html", user=None):
        return self.render(template, form=form, user=user)
