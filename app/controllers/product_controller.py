from flask import request, jsonify, render_template, redirect, url_for
from app.services.product_service import ProductService
from app.utils.forms.product_form import ProductForm
from app.controllers.base_auth_controller import BaseController

class ProductController(BaseController):
    @staticmethod
    def list_products():
        """Lista todos los productos en la vista de administración"""
        products = ProductService.get_all_products()
        return render_template("admin/products.html", products=products)

    @staticmethod
    def new_product_form():
        """Muestra el formulario de creación de productos"""
        form = ProductForm()
        categories = ProductService.get_all_categories()  # Obtener categorías para el select
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]
        return render_template("admin/product_form.html", form=form)

    @staticmethod
    def create_product():
        """Crea un nuevo producto"""
        form = ProductForm()
        categories = ProductService.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        if request.method == "POST" and form.validate_on_submit():
            data = {
                "nombre": form.nombre.data,
                "categoria_id": form.categoria_id.data,
                "precio": form.precio.data
            }

            result = ProductService.create_product(data)

            if result["success"]:
                return redirect(url_for("admin.list_products"))

            return render_template("admin/product_form.html", form=form, error=result["message"])

        return render_template("admin/product_form.html", form=form)
