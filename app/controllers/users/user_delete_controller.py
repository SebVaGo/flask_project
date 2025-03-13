from app.controllers.users.base_user_controller import BaseUserController


class UserDeleteController(BaseUserController):

    def delete_user(self, user_id):
        resultado = self.user_service.delete_user(user_id)
        return self.json_response(resultado["success"], resultado["message"], status=200 if resultado["success"] else 400)
