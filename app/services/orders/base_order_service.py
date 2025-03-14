import logging
from app.models.order_model import OrderModel
from app.models.user_model import UserModel
from app.models.product_model import ProductModel
from app.utils.db_session_manager import DBSessionManager


class BaseOrderService:
    def __init__(self):
        self.db_manager = DBSessionManager()
        self.order_model = OrderModel
        self.user_model = UserModel
        self.product_model = ProductModel

    def _get_next_order_id(self):
        try:
            last_order = self.order_model.query.order_by(
                self.order_model.orden_id.desc()
            ).first()
            return (last_order.orden_id + 1) if last_order else 1
        except Exception as e:
            logging.error(f"Error in _get_next_order_id: {str(e)}")
            raise Exception("Error interno al obtener el siguiente ID de orden.")
