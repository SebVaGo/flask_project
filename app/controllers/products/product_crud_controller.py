import logging

from flask import request, flash, url_for, redirect
from app.utils.forms.csrf_form import CSRFForm
from app.utils.forms.product_form import ProductForm
from app.controllers.products.base_product_controller import BaseProductController

class ProductCrudController(BaseProductController):

    def list_products(self):
        products = self.product_service.get_all_products()
        form = CSRFForm()
        return self.render("admin/products.html", products=products, form=form)
    
    def create_product(self):
        """Crea un nuevo producto."""
        # Si se envía información (POST), usamos request.form para conservar los datos
        form = ProductForm(request.form)  
        categories = self.category_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        if request.method == "GET":
            # Renderizamos el formulario vacío
            return self.render_product_form(form)
        
        # Si es POST, validamos el formulario
        if not form.validate():
            flash("Errores de validación", "danger")
            # Re-renderizamos el formulario con los datos ingresados y errores
            return self.render_product_form(form)

        # Extraemos los datos del formulario
        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        # Llamamos al servicio para crear el producto (sin product_id para creación)
        result, status_code = self.product_service.save_product(data)
        
        # Si ocurre algún error en el guardado, se puede mostrar un mensaje y re-renderizar el formulario
        if not result["success"]:
            flash(result["message"], "danger")
            return self.render_product_form(form)

        flash(result["message"], "success")
        # Redirecciona a la lista de productos u otra vista luego de la creación exitosa
    
        return self.json_response(result["success"], result["message"], status=status_code)

    def edit_product(self, product_id):
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
            "precio": form.precio.data
        }

        result, status_code = self.product_service.save_product(data, product_id)
        if result["success"]:
            flash("Producto actualizado correctamente.", "success")
        else:
            flash(result["message"], "danger")
        return self.json_response(result["success"], result["message"], status=status_code)

    def delete_product(self, product_id):
        result = self.product_service.delete_product(product_id)
        return self.json_response(result["success"], result["message"], status=200 if result["success"] else 400)
