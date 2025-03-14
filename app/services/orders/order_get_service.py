from app.config import db
from app.services.orders.base_order_service import BaseOrderService


class OrderQueryService(BaseOrderService):

    def __init__(self):
        super().__init__()

    def get_order_item(self, session, orden_id, producto_id):
        return session.query(self.order_model).filter_by(
            orden_id=orden_id, producto_id=producto_id
        ).first()
    
    def get_all_order_items(self, session, orden_id):
        return session.query(self.order_model).filter_by(orden_id=orden_id).all()
    
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
            "productos": []
        }

        for row in rows:
            order_data["productos"].append({
                "producto_id": row.producto_id,
                "producto_nombre": row.producto_nombre,
                "cantidad": row.cantidad
            })
        return order_data


    