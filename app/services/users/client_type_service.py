from app.models.client_tipe_model import ClientTypeModel


class ClientTypeService:

    @staticmethod
    def get_all_types():
        return ClientTypeModel.query.all()

    @staticmethod
    def get_type_by_id(tipo_cliente_id):
        return ClientTypeModel.query.get(tipo_cliente_id)