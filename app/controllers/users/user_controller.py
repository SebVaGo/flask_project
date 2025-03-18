from app.controllers.users.user_crud_controller import UserCrudController
from app.utils.decorators import admin_and_login_required_for_all_methods


@admin_and_login_required_for_all_methods
class UserController(UserCrudController):
    pass
