from werkzeug.security import generate_password_hash
from app.repositories.user_repository import UserRepository
from app.repositories.password_repository import PasswordRepository
from app.models.client_tipe_model import ClientType
from app.config import db
import logging

class UserService: 
    @staticmethod
    def get_all_tipe_user():
        try:
            return ClientType.query.all()
        except Exception as e:
            logging.error(f"Error al obtener tipos de usuario: {str(e)}")
            return []

    @staticmethod
    def create_user(data):
        print("Datos recibidos en create_user:", data) 

        try:
            if UserRepository.get_user_by_email(data["correo"]):
                return {"success": False, "message": "El correo ya está en uso."}
            
            tipo_cliente = ClientType.query.get(data["tipo_cliente_id"])
            if not tipo_cliente:
                return {"success": False, "message": "El tipo de cliente no existe"}       
            
            password_hash = generate_password_hash(data.pop("password"))

            user = UserRepository.create_user_with_password(data, password_hash)

            return {"success": True, "message": "Usuario registrado exitosamente"}
        except Exception as e:
            logging.error(f"Error inesperado en UserService: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}
            
    @staticmethod
    def get_all_users():
        try:
            return UserRepository.get_all_users()
        except Exception as e:
            logging.error(f"Error al obtener usuarios: {str(e)}")
            return []

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return UserRepository.get_user_by_id(user_id)
        except Exception as e:
            logging.error(f"Error al obtener usuario {user_id}: {str(e)}")
            return None

    @staticmethod
    def actualizar_usuario(user_id, data):
        try:
            usuario = UserRepository.get_user_by_id(user_id)
            if not usuario:
                return {"success": False, "message": "Usuario no encontrado."}, 404

            # Verificar si el correo se quiere actualizar y no está en uso
            nuevo_correo = data.get("correo")
            if nuevo_correo and nuevo_correo != usuario.correo:
                usuario_existente = UserRepository.get_user_by_email(nuevo_correo)
                if usuario_existente and usuario_existente.id != user_id:
                    return {"success": False, "message": "El correo ya está en uso por otro usuario."}, 400
                
            # Verificar si el tipo de cliente existe
            if "tipo_cliente_id" in data:
                tipo_cliente = ClientType.query.get(data["tipo_cliente_id"])
                if not tipo_cliente:
                    return {"success": False, "message": "Tipo de cliente inválido."}, 400

            # Extraer y eliminar la nueva contraseña del diccionario
            nueva_password = data.pop("nueva_password", None)

            # Iniciar la transacción manualmente
            try:
                actualizado = UserRepository.update_by_id(user_id, data)

                # Si hay una nueva contraseña, actualizarla
                if nueva_password:
                    password_hash = generate_password_hash(nueva_password)
                    if not PasswordRepository.update_password(user_id, password_hash):
                        raise Exception("Error al actualizar la contraseña")

                db.session.commit()  # Confirmar los cambios en la base de datos
                return {"success": True, "message": "Usuario actualizado correctamente."}, 200

            except Exception as e:
                db.session.rollback()  # Revertir cambios en caso de error
                raise e  # Relanzar la excepción para que sea capturada en el `except` externo

        except Exception as e:
            logging.error(f"Error al actualizar usuario {user_id}: {e}")
            return {"success": False, "message": "Error interno del servidor."}, 500
        
    @staticmethod
    def delete_user(user_id):
        try:
            if UserRepository.delete_by_id(user_id):
                return {"success": True, "message": "Usuario eliminado correctamente."}
            return {"success": False, "message": "No se pudo eliminar el usuario."}
        except Exception as e:
            logging.error(f"Error al eliminar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor."}
