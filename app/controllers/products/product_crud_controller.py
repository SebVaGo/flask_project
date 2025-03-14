import logging
from flask import request, flash, url_for, redirect
from app.utils.forms.csrf_form import CSRFForm
from app.utils.forms.product_form import ProductForm
from app.controllers.products.base_product_controller import BaseProductController


class ProductCrudController(BaseProductController):

    def list_products(self):
        try:
            products = self.product_service.get_all_products()
            form = CSRFForm()
            return self.render("admin/products.html", products=products, form=form)
        except Exception as e:
            logging.error(f"Error en list_products: {str(e)}")
            flash("Ocurrió un error al obtener los productos.", "danger")
            return self.render("admin/products.html", products=[], form=CSRFForm())

    def create_product(self):
        """Crea un nuevo producto."""
        try:
            form = ProductForm(request.form)
            categories = self.category_service.get_all_categories()
            form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

            if request.method == "GET":
                return self.render_product_form(form)

            errors = self.validate_form(form)
            if errors:
                flash("Errores de validación", "danger")
                return self.json_response(False, "Errores de validación", errors=errors, status=400)

            data = {
                "nombre": form.nombre.data,
                "categoria_id": form.categoria_id.data,
                "precio": form.precio.data,
            }

            result, status_code = self.product_service.save_product(data)
            if not result["success"]:
                flash("Producto creado correctamente.", "success")
                return self.render_product_form(form)

            flash(result["message"], "success")
            return self.json_response(result["success"], result["message"], status=status_code)
        except Exception as e:
            logging.error(f"Error en create_product: {str(e)}")
            flash("Ocurrió un error al crear el producto.", "danger")
            return self.json_response(False, "Error interno del servidor", status=500)

    def edit_product(self, product_id):
        try:
            product = self.product_service.get_product_by_id(product_id)
            if not product:
                return self.json_response(False, "Producto no encontrado", status=404)

            form = ProductForm(obj=product)
            categories = self.category_service.get_all_categories()
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
                "precio": form.precio.data,
            }

            result, status_code = self.product_service.save_product(data, product_id)
            if result["success"]:
                flash("Producto actualizado correctamente.", "success")
            else:
                flash(result["message"], "danger")
            return self.json_response(result["success"], result["message"], status=status_code)
        except Exception as e:
            logging.error(f"Error en edit_product: {str(e)}")
            flash("Ocurrió un error actualizando el producto.", "danger")
            return self.json_response(False, "Error interno del servidor", status=500)

    def delete_product(self, product_id):
        try:
            result = self.product_service.delete_product(product_id)
            return self.json_response(
                result["success"],
                result["message"],
                status=200 if result["success"] else 400
            )
        except Exception as e:
            logging.error(f"Error en delete_product: {str(e)}")
            return self.json_response(False, "Error interno del servidor", status=500)
