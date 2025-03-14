import logging
from app.config import db
from app.services.users.base_user_service import BaseUserService
from app.services.users.client_type_service import ClientTypeService
from app.services.users.password_service import PasswordService
from app.services.users.user_save_service import UserSaveService


class UserService(BaseUserService):

    def __init__(self):
        super().__init__()
        self.password_service = PasswordService()
        self.client_type_service = ClientTypeService()
        self.user_save_service = UserSaveService()

    def get_all_users(self):
        try:
            return self.user_model.query.all()
        except Exception as e:
            logging.error(f"Error al obtener usuarios: {str(e)}")
            return []

    def get_user_by_id(self, user_id):
        try:
            return self.user_model.query.get(user_id)
        except Exception as e:
            logging.error(f"Error al obtener usuario {user_id}: {str(e)}")
            return None

    def save_user(self, data, user_id=None):
        try:
            return self.user_save_service.save_user(data, user_id)
        except Exception as e:
            logging.error(f"Error en save_user: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500

    def delete_user(self, user_id):
        usuario = self.user_model.query.get(user_id)
        if not usuario:
            return {"success": False, "message": "Usuario no encontrado"}

        try:
            db.session.query(self.user_model).filter_by(id=user_id).delete()
            db.session.delete(usuario)
            db.session.commit()
            return {"success": True, "message": "Usuario eliminado correctamente"}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al eliminar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}
