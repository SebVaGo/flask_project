from app.config import db
from app.models.order_model import OrderModel
from app.models.product_model import ProductModel
from app.models.user_model import UserModel


class OrderQueryService:

    def __init__(self):
        self.order_model = OrderModel
        self.product_model = ProductModel
        self.user_model = UserModel

    def get_all_orders(self):
        return (
            db.session.query(
                self.order_model.orden_id,
                self.user_model.primer_nombre.label("usuario_nombre"),
                self.product_model.nombre.label("producto_nombre"),
                self.order_model.producto_id,
                self.order_model.cantidad,
                self.order_model.fecha_creacion
            )
            .join(self.user_model, self.order_model.usuario_id == self.user_model.id)
            .join(self.product_model, self.order_model.producto_id == self.product_model.id)
            .order_by(self.order_model.orden_id.desc())
            .all()
        )
