from app.config import db
from app.services.products.product_save_service import ProductSaveService
from app.services.products.base_product_service import BaseProductService
from sqlalchemy import update


class ProductService(BaseProductService):

    def __init__(self):
        super().__init__()
        self.product_save_service = ProductSaveService()

    #Crear o acutalizar
    def save_product(self, data, product_id=None):
        return self.product_save_service.save_product(data, product_id)

    #Devolver todos los productos
    def get_all_products(self):
        return db.session.query(
            self.product_model.id,
            self.product_model.nombre,
            self.product_model.precio,
            self.category_model.nombre.label("categoria")
        ).join(self.category_model).all()

    def get_product_by_id(self, product_id):
        return db.session.query(
            self.product_model.id,
            self.product_model.categoria_id,
            self.category_model.nombre.label("categoria"),
            self.product_model.nombre,
            self.product_model.precio
        ).join(self.category_model).filter(self.product_model.id == product_id).first()

    
    def delete_product(self, product_id):
        product = self.product_model.query.get(product_id)
        if not product:
            return {"success": False, "message": "Producto no encontrado"}

        try:
            self.delete_orders_by_product(product_id)
            db.session.delete(product)
            self.db_manager.commit()
            return {"success": True, "message": "Producto eliminado correctamente"}
        except Exception as e:
            return {"success": False, "message": f"Error al eliminar el producto: {str(e)}"}

    def delete_orders_by_product(self, product_id):
        db.session.query(self.order_model).filter_by(producto_id=product_id).delete()