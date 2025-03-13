from werkzeug.security import generate_password_hash
from app.config import db
from app.models.user_model import User
from app.models.password_model import Password
from app.models.client_tipe_model import ClientType
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
            # Verificar si el correo ya existe
            if User.query.filter_by(correo=data["correo"]).first():
                return {"success": False, "message": "El correo ya está en uso."}
            
            # Verificar si el tipo de cliente existe
            tipo_cliente = ClientType.query.get(data["tipo_cliente_id"])
            if not tipo_cliente:
                return {"success": False, "message": "El tipo de cliente no existe"}       
            
            # Hash de la contraseña
            password_hash = generate_password_hash(data.pop("password"))

            # Crear usuario
            user = User(**data)
            db.session.add(user)
            db.session.flush()  # Permitir que el usuario tenga ID antes de agregar la contraseña

            # Crear contraseña vinculada
            password_entry = Password(id_usuario=user.id, password_hash=password_hash)
            db.session.add(password_entry)

            # Confirmar transacción
            db.session.commit()
            db.session.expunge_all()  # Limpiar la sesión

            return {"success": True, "message": "Usuario registrado exitosamente"}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error inesperado en UserService: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}
            
    @staticmethod
    def get_all_users():
        try:
            return User.query.all()
        except Exception as e:
            logging.error(f"Error al obtener usuarios: {str(e)}")
            return []

    @staticmethod
    def get_user_by_id(user_id):
        try:
            return User.query.get(user_id)
        except Exception as e:
            logging.error(f"Error al obtener usuario {user_id}: {str(e)}")
            return None

    @staticmethod
    def actualizar_usuario(user_id, data):
        try:
            usuario = User.query.get(user_id)
            if not usuario:
                return {"success": False, "message": "Usuario no encontrado."}, 404

            # Verificar si el correo se quiere actualizar y ya existe
            nuevo_correo = data.get("correo")
            if nuevo_correo and nuevo_correo != usuario.correo:
                usuario_existente = User.query.filter_by(correo=nuevo_correo).first()
                if usuario_existente and usuario_existente.id != user_id:
                    return {"success": False, "message": "El correo ya está en uso por otro usuario."}, 400
                
            # Verificar si el tipo de cliente existe
            if "tipo_cliente_id" in data:
                tipo_cliente = ClientType.query.get(data["tipo_cliente_id"])
                if not tipo_cliente:
                    return {"success": False, "message": "Tipo de cliente inválido."}, 400

            # Extraer y eliminar la nueva contraseña del diccionario
            nueva_password = data.pop("nueva_password", None)

            # Actualizar usuario
            for key, value in data.items():
                if hasattr(usuario, key) and value:
                    setattr(usuario, key, value)

            # Si hay una nueva contraseña, actualizarla
            if nueva_password:
                password_hash = generate_password_hash(nueva_password)
                password_entry = Password.query.filter_by(id_usuario=user_id).first()
                if password_entry:
                    password_entry.password_hash = password_hash
                else:
                    new_password_entry = Password(id_usuario=user_id, password_hash=password_hash)
                    db.session.add(new_password_entry)

            # Guardar cambios
            db.session.commit()
            return {"success": True, "message": "Usuario actualizado correctamente."}, 200

        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al actualizar usuario {user_id}: {e}")
            return {"success": False, "message": "Error interno del servidor."}, 500
        
    @staticmethod
    def delete_user(user_id):
        try:
            usuario = User.query.get(user_id)
            if not usuario:
                return {"success": False, "message": "Usuario no encontrado."}

            # Eliminar usuario
            db.session.delete(usuario)
            db.session.commit()

            return {"success": True, "message": "Usuario eliminado correctamente."}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al eliminar usuario {user_id}: {str(e)}")
            return {"success": False, "message": "Error interno del servidor."}
