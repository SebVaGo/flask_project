from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.repositories.password_repository import PasswordRepository
import logging

class UserService: 
    @staticmethod
    def create_user(data):
        """Registra un usuario en la base de datos"""
        try:
            if UserRepository.get_user_by_email(data["correo"]):
                return {"success": False, "message": "El correo ya está en uso."}

            password_hash = generate_password_hash(data.pop("password"))  # 🔥 Hash de la contraseña

            user = UserRepository.create_user(data)
            if user:
                PasswordRepository.create_password(user.id, password_hash)
                return {"success": True, "message": "Usuario registrado exitosamente."}

            return {"success": False, "message": "Error al registrar usuario."}
        except Exception as e:
            logging.error(f"Error al registrar usuario: {str(e)}")
            return {"success": False, "message": "Error interno del servidor."}

    @staticmethod
    def get_all_users():
        """Obtiene la lista de todos los usuarios"""
        try:
            return UserRepository.get_all_users()
        except Exception as e:
            logging.error(f"Error al obtener usuarios: {str(e)}")
            return []

    @staticmethod
    def get_user_by_id(user_id):
        """Obtiene un usuario por su ID"""
        try:
            return UserRepository.get_user_by_id(user_id)
        except Exception as e:
            logging.error(f"Error al obtener usuario {user_id}: {str(e)}")
            return None

    @staticmethod
    def actualizar_usuario(user_id, data):
        """Actualiza los datos de un usuario"""
        try:
            if UserRepository.update_by_id(user_id, data):
                return {"success": True, "message": "Usuario actualizado correctamente."}
            return {"success": False, "message": "No se pudo actualizar el usuario."}
        except Exception as e:
            logging.error(f"Error al actualizar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor."}

    @staticmethod
    def delete_user(user_id):
        """Elimina físicamente un usuario"""
        try:
            if UserRepository.delete_by_id(user_id):
                return {"success": True, "message": "Usuario eliminado correctamente."}
            return {"success": False, "message": "No se pudo eliminar el usuario."}
        except Exception as e:
            logging.error(f"Error al eliminar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor."}
