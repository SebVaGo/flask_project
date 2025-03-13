from app.controllers.users.base_user_controller import BaseUserController
from app.utils.forms.csrf_form import CSRFForm


class UserListController(BaseUserController):

    def get_users(self):
        users = self.user_service.get_all_users()
        form = CSRFForm()
        return self.render("users.html", users=users, form=form)
