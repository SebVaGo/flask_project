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
    
    def get_order_by_id(self, order_id):
        rows = (
            db.session.query(
                self.order_model.orden_id,
                self.order_model.usuario_id,
                self.user_model.primer_nombre.label("usuario_nombre"),
                self.product_model.nombre.label("producto_nombre"),
                self.order_model.producto_id,
                self.order_model.cantidad,
                self.order_model.fecha_creacion
            )
            .join(self.user_model, self.order_model.usuario_id == self.user_model.id)
            .join(self.product_model, self.order_model.producto_id == self.product_model.id)
            .filter(self.order_model.orden_id == order_id)
            .all()
        )

        if not rows:
            return None  # No existe la orden

        order_data = {
            "orden_id": rows[0].orden_id,
            "usuario_id": rows[0].usuario_id,
            "usuario_nombre": rows[0].usuario_nombre,
            "fecha_creacion": rows[0].fecha_creacion,
            # Cambia "items" por "productos" para evitar conflicto:
            "productos": []
        }

        for row in rows:
            order_data["productos"].append({
                "producto_id": row.producto_id,
                "producto_nombre": row.producto_nombre,
                "cantidad": row.cantidad
            })

        return order_data
