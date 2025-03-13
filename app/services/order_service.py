from app.config import db

class OrderService:
    def __init__(self):
        self.db = db

    def get_next_order_id(self):
        from app.models.order_model import Order  # 🔥 Import dentro del método
        last_order = self.db.session.query(Order).order_by(Order.__table__.c.orden_id.desc()).first()
        return (last_order.orden_id + 1) if last_order else 1

    def create_order(self, data):
        from app.models.order_model import Order  # 🔥 Import dentro del método
        usuario_id = data["usuario_id"]
        productos = data["products"]
        orden_id = self.get_next_order_id()

        orders_to_add = []
        for producto in productos:
            order = Order(
                orden_id=orden_id,
                usuario_id=usuario_id,
                producto_id=producto["producto_id"],
                cantidad=producto["cantidad"]
            )
            orders_to_add.append(order)

        try:
            self.db.session.add_all(orders_to_add)
            self.db.session.commit()
            return {"success": True, "orden_id": orden_id}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al guardar la orden: {str(e)}"}

    def get_all_orders(self):
        from app.models.order_model import Order  # 🔥 Import dentro del método
        from app.models.product_model import Product
        from app.models.user_model import User

        orders = (
            self.db.session.query(
                Order.__table__.c.orden_id,
                User.__table__.c.primer_nombre.label("usuario_nombre"),
                Product.__table__.c.nombre.label("producto_nombre"),
                Order.__table__.c.producto_id,
                Order.__table__.c.cantidad,
                Order.__table__.c.fecha_creacion
            )
            .join(User, Order.__table__.c.usuario_id == User.__table__.c.id)
            .join(Product, Order.__table__.c.producto_id == Product.__table__.c.id)
            .order_by(Order.__table__.c.orden_id.desc())
            .all()
        )

        return orders

    def update_order_quantity(self, orden_id, producto_id, nueva_cantidad):
        from app.models.order_model import Order  # 🔥 Import dentro del método
        order = self.db.session.query(Order).filter_by(orden_id=orden_id, producto_id=producto_id).first()

        if not order:
            return {"success": False, "message": "La orden especificada no existe."}

        try:
            order.cantidad = nueva_cantidad
            self.db.session.commit()
            return {"success": True, "message": "Cantidad actualizada correctamente."}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al actualizar la cantidad: {str(e)}"}

    def delete_order_product(self, orden_id, producto_id):
        from app.models.order_model import Order  # 🔥 Import dentro del método
        order = self.db.session.query(Order).filter_by(orden_id=orden_id, producto_id=producto_id).first()

        if not order:
            return {"success": False, "message": "Producto en la orden no encontrado."}

        try:
            self.db.session.delete(order)
            self.db.session.commit()
            return {"success": True, "message": "Producto eliminado correctamente."}
        except Exception as e:
            self.db.session.rollback()
            return {"success": False, "message": f"Error al eliminar el producto: {str(e)}"}
