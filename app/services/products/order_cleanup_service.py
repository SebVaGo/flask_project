from app.config import db
from app.models.order_model import OrderModel


class OrderCleanupService:

    def __init__(self):
        self.order_model = OrderModel

    def delete_orders_by_product(self, product_id):
        db.session.query(self.order_model).filter_by(producto_id=product_id).delete()
