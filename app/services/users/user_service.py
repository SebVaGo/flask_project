import logging

from app.config import db

from app.models.user_model import UserModel
from app.models.order_model import OrderModel

from app.services.users.client_type_service import ClientTypeService
from app.services.users.password_service import PasswordService


class UserService:

    def __init__(self):
        self.password_service = PasswordService()
        self.client_type_service = ClientTypeService()
        self.user_model = UserModel()

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

    def create_user(self, data):
        try:
            if UserModel.query.filter_by(correo=data["correo"]).first():
                return {"success": False, "message": "El correo ya está en uso."}

            tipo_cliente = self.client_type_service.get_type_by_id(data["tipo_cliente_id"])
            if not tipo_cliente:
                return {"success": False, "message": "El tipo de cliente no existe"}

            password = data.pop("password")
            user = UserModel(**data, status="activo")
            db.session.add(user)
            db.session.flush()

            self.password_service.create_password(user.id, password)
            db.session.commit()
            return {"success": True, "message": "Usuario registrado exitosamente"}
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error inesperado en UserService: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}

    def update_user(self, user_id, data):
        try:
            usuario = UserModel.query.get(user_id)
            if not usuario:
                return {"success": False, "message": "Usuario no encontrado."}, 404

            nuevo_correo = data.get("correo")
            if nuevo_correo and nuevo_correo != usuario.correo:
                if UserModel.query.filter_by(correo=nuevo_correo).first():
                    return {"success": False, "message": "El correo ya está en uso por otro usuario."}, 400

            if "tipo_cliente_id" in data and not self.client_type_service.get_type_by_id(data["tipo_cliente_id"]):
                return {"success": False, "message": "Tipo de cliente inválido."}, 400

            nueva_password = data.pop("nueva_password", None)

            for key, value in data.items():
                if hasattr(usuario, key) and value:
                    setattr(usuario, key, value)

            if nueva_password:
                self.password_service.update_password(user_id, nueva_password)

            db.session.commit()
            return {"success": True, "message": "Usuario actualizado correctamente."}, 200
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error al actualizar usuario {user_id}: {e}")
            return {"success": False, "message": "Error interno del servidor."}, 500

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
