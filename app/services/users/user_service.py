import logging
from app.config import db
from app.models.user_model import UserModel
from app.models.order_model import OrderModel
from app.services.users.client_type_service import ClientTypeService
from app.services.users.password_service import PasswordService
from app.services.users.user_save_service import UserSaveService


class UserService:

    def __init__(self):

        self.password_service = PasswordService()
        self.client_type_service = ClientTypeService()
        self.user_model = UserModel()
        self.user_save_service = UserSaveService(self.client_type_service, self.password_service)

    def get_all_users(self):
        try:
            return UserModel.query.all()
        except Exception as e:
            logging.error(f"Error al obtener usuarios: {str(e)}")
            return []

    def get_user_by_id(self, user_id):
        try:
            return UserModel.query.get(user_id)
        except Exception as e:
            logging.error(f"Error al obtener usuario {user_id}: {str(e)}")
            return None
    
    def save_user(self, data, user_id=None):
        return self.user_save_service.save_user(data, user_id)

    def delete_user(self, user_id):
        usuario = self.user_model.query.get(user_id)
        if not usuario:
            return {"success": False, "message": "Usuario no encontrado"}

        try:
            db.session.query(OrderModel).filter_by(usuario_id=user_id).delete()

            db.session.delete(usuario)
            db.session.commit()
            return {"success": True, "message": "Usuario eliminado correctamente"}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al eliminar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}
