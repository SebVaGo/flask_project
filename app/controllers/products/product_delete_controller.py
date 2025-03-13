from app.controllers.products.base_product_controller import BaseProductController


class ProductDeleteController(BaseProductController):

    def delete_product(self, product_id):
        result = self.product_service.delete_product(product_id)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)
