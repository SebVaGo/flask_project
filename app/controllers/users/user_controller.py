from app.controllers.users.user_create_controller import UserCreateController
from app.controllers.users.user_edit_controller import UserEditController
from app.controllers.users.user_delete_controller import UserDeleteController
from app.controllers.users.user_list_controller import UserListController
from app.services.users.user_service import UserService


class UserController(UserCreateController, UserEditController, UserDeleteController, UserListController):
    pass
