import logging
from app.config import db
from app.services.users.base_user_service import BaseUserService
from app.services.users.client_type_service import ClientTypeService
from app.services.users.password_service import PasswordService


class UserSaveService(BaseUserService):

    def __init__(self):
        super().__init__()
        self.client_type_service = ClientTypeService()
        self.password_service = PasswordService()

    def _validate_email(self, session, email, user_id=None):
        try:
            if email:
                query = session.query(self.user_model).filter_by(correo=email)
                if user_id is not None:
                    query = query.filter(self.user_model.id != user_id)
                if query.first():
                    return "El correo ya está en uso."
            return None
        except Exception as e:
            logging.error(f"Error in _validate_email: {str(e)}")
            raise Exception("Error al validar el correo electrónico.")

    def save_user(self, data, user_id=None):
        session = db.session
        try:
            is_update = user_id is not None

            # 1. Obtener (o validar) usuario si es actualización
            usuario, error, status_code = self._get_user_if_update(session, user_id)
            if error:
                return error, status_code

            # 2. Validar email y tipo de cliente
            error, status_code = self._check_email_and_client(session, data, user_id)
            if error:
                return error, status_code

            # 3. Extraer la contraseña según sea update o create
            nueva_password = self.password_service.extract_password(data, is_update)

            # 4. Actualizar usuario existente o crear uno nuevo
            if is_update:
                self._update_existing_user(usuario, data)
            else:
                usuario = self._create_new_user(session, data)

            # 5. Manejar contraseña
            if nueva_password:
                self._update_password(session, usuario, nueva_password, is_update)

            session.commit()
            mensaje = (
                "Usuario actualizado correctamente."
                if is_update
                else "Usuario registrado exitosamente"
            )
            return {"success": True, "message": mensaje}, 200 if is_update else 201

        except Exception as e:
            session.rollback()
            logging.error(f"Error en operación de usuario: {str(e)}")
            return {"success": False, "message": "Error interno del servidor"}, 500
        finally:
            session.close()

    def _get_user_if_update(self, session, user_id):
        try:
            if user_id is not None:
                usuario = session.query(self.user_model).get(user_id)
                if not usuario:
                    return None, {"success": False, "message": "Usuario no encontrado."}, 404
                return usuario, None, None
            return None, None, None
        except Exception as e:
            logging.error(f"Error in _get_user_if_update: {str(e)}")
            raise Exception("Error al obtener el usuario para actualización.")

    def _check_email_and_client(self, session, data, user_id=None):
        try:
            email_error = self._validate_email(session, data.get("correo"), user_id)
            if email_error:
                return {"success": False, "message": email_error}, 400

            client_error = self.client_type_service.validate_client_type(data)
            if client_error:
                return {"success": False, "message": client_error}, 400

            return None, None
        except Exception as e:
            logging.error(f"Error in _check_email_and_client: {str(e)}")
            raise Exception("Error al validar email y tipo de cliente.")

    def _update_existing_user(self, usuario, data):
        try:
            for key, value in data.items():
                if hasattr(usuario, key) and value is not None:
                    setattr(usuario, key, value)
        except Exception as e:
            logging.error(f"Error in _update_existing_user: {str(e)}")
            raise Exception("Error al actualizar el usuario existente.")

    def _create_new_user(self, session, data):
        try:
            usuario = self.user_model(**data, status="activo")
            session.add(usuario)
            session.flush()
            return usuario
        except Exception as e:
            logging.error(f"Error in _create_new_user: {str(e)}")
            raise Exception("Error al crear un nuevo usuario.")

    def _update_password(self, session, usuario, nueva_password, is_update):
        try:
            if is_update:
                self.password_service.update_password(session, usuario.id, nueva_password)
            else:
                self.password_service.create_password(session, usuario.id, nueva_password)
        except Exception as e:
            logging.error(f"Error in _update_password: {str(e)}")
            raise Exception("Error al actualizar la contraseña.")
