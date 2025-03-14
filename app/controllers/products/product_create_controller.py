from flask import request, flash
from app.controllers.products.base_product_controller import BaseProductController
from app.utils.forms.product_form import ProductForm


class ProductCreateController(BaseProductController):
    """Maneja la creación de productos."""

    def new_product_form(self):
        """Muestra el formulario para crear un nuevo producto."""
        form = ProductForm()
        categories = self.product_service.category_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]
        return self.render_product_form(form)

    def create_product(self):
        """Crea un nuevo producto."""
        form = ProductForm()
        categories = self.product_service.category_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        errors = self.validate_form(form)
        if errors:
            flash("Errores de validación", "danger")
            return self.json_response(False, "Errores de validación", errors=errors, status=400)

        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        # Se llama a la función unificada sin product_id para creación
        result, status_code = self.product_service.save_product(data)
        return self.json_response(result["success"], result["message"], status=status_code)