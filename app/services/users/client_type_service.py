import logging
from app.services.users.base_user_service import BaseUserService


class ClientTypeService(BaseUserService):

    def __init__(self):
        super().__init__()

    def get_all_types(self):
        try:
            return self.client_type_model.query.all()
        except Exception as e:
            logging.error(f"Error in get_all_types: {str(e)}")
            raise Exception("Ocurrió un error al obtener los tipos de cliente.")

    def get_type_by_id(self, tipo_cliente_id):
        try:
            return self.client_type_model.query.get(tipo_cliente_id)
        except Exception as e:
            logging.error(f"Error in get_type_by_id: {str(e)}")
            raise Exception("Ocurrió un error al obtener el tipo de cliente.")

    def validate_client_type(self, data):
        try:
            if "tipo_cliente_id" in data:
                tipo_cliente = self.get_type_by_id(data["tipo_cliente_id"])
                if not tipo_cliente:
                    return "El tipo de cliente no existe"
            return None
        except Exception as e:
            logging.error(f"Error in validate_client_type: {str(e)}")
            raise Exception("Ocurrió un error al validar el tipo de cliente.")
