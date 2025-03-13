from app import db
from app.models.order_model import Order
from app.models.product_model import Product
from app.models.user_model import User

class OrderService:

    def __init__(self):
        self.db = db

    def get_next_order_id(self):
        last_order = self.db.session.query(Order).order_by(Order.orden_id.desc()).first()
        return (last_order.orden_id + 1) if last_order else 1

    def create_order(self, data):
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
        orders = (
            self.db.session.query(
                Order.orden_id,
                User.primer_nombre.label("usuario_nombre"),
                Product.nombre.label("producto_nombre"),
                Order.producto_id,
                Order.cantidad,
                Order.fecha_creacion
            )
            .join(User, Order.usuario_id == User.id)
            .join(Product, Order.producto_id == Product.id)
            .order_by(Order.orden_id.desc())
            .all()
        )

        return orders

    def update_order_quantity(self, orden_id, producto_id, nueva_cantidad):
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
