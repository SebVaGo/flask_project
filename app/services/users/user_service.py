import logging
from app.config import db
from app.services.users.base_user_service import BaseUserService
from app.services.users.client_type_service import ClientTypeService
from app.services.users.password_service import PasswordService
from app.services.users.user_save_service import UserSaveService
from app.utils.db_session_manager import AltDBSessionManager

class UserService(BaseUserService):

    def __init__(self):
        super().__init__()
        self.password_service = PasswordService()
        self.client_type_service = ClientTypeService()
        self.user_save_service = UserSaveService()

    def get_all_users(self):
        try:
            with AltDBSessionManager() as session:
                users = session.query(self.user_model).all()
                user_list = []
                for user in users:
                    user_dict = self._user_to_dict(user)
                    user_list.append(user_dict)
                return user_list
        except Exception as e:
            logging.error(f"Error al obtener usuarios: {str(e)}")
            return []

    def get_user_by_id(self, user_id):
        try:
            with AltDBSessionManager() as session:
                user = session.query(self.user_model).get(user_id)
                if user:
                    return self._user_to_dict(user)
                return None
        except Exception as e:
            logging.error(f"Error al obtener usuario {user_id}: {str(e)}")
            return None
    
    def _user_to_dict(self, user):
        user_dict = {}
        columns = ['id', 'primer_nombre', 'segundo_nombre', 'apellido_paterno', 
                   'apellido_materno', 'correo', 'telefono', 'fecha_creacion', 
                   'fecha_actualizacion', 'status', 'tipo_cliente_id']
        
        for column in columns:
            if hasattr(user, column):
                user_dict[column] = getattr(user, column)
        
        return user_dict
    
    def save_user(self, data, user_id=None):
        try:
            return self.user_save_service.save_user(data, user_id)
        except Exception as e:
            logging.error(f"Error en save_user: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500

    def delete_user(self, user_id):
        try:
            with AltDBSessionManager() as session:
                usuario = session.query(self.user_model).get(user_id)
                if not usuario:
                    return {"success": False, "message": "Usuario no encontrado"}
                session.delete(usuario)
                return {"success": True, "message": "Usuario eliminado correctamente"}
        except Exception as e:
            logging.error(f"Error al eliminar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}
