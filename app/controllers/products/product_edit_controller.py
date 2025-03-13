from flask import request, flash
from app.controllers.products.base_product_controller import BaseProductController
from app.utils.forms.product_form import ProductForm


class ProductEditController(BaseProductController):

    def edit_product(self, product_id):
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            return self.json_response(False, "Producto no encontrado", status=404)

        form = ProductForm(obj=product)
        categories = self.product_service.category_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        if request.method == "GET":
            return self.render_product_form(form, product=product)

        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        result = self.product_service.update_product(product_id, data)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)
