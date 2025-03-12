from flask import request, jsonify, render_template, redirect, url_for
from app.services.product_service import ProductService
from app.utils.forms.product_form import ProductForm
from app.controllers.base_auth_controller import BaseController
from flask_wtf.csrf import generate_csrf
from app.utils.auth_decorator import require_authentication


class ProductController:
    @staticmethod
    @require_authentication
    def list_products():

        """Lista todos los productos en la vista de administración"""
        products = ProductService.get_all_products()
        csrf_token = generate_csrf()  # 🔹 Generar el token CSRF en el backend
        return render_template("admin/products.html", products=products, csrf_token=csrf_token)

    @staticmethod
    @require_authentication
    def new_product_form():
        
        """Muestra el formulario de creación de productos"""
        form = ProductForm()
        categories = ProductService.get_all_categories()  # Obtener categorías para el select

        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]
        
        return render_template("admin/product_form.html", form=form)

    @staticmethod
    @require_authentication
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
    
    @staticmethod
    @require_authentication
    def delete_product(product_id):

        result = ProductService.delete_product(product_id)
        if result["success"]:
            return jsonify({"success": True, "message": "Producto eliminado correctamente"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400
    
    @staticmethod
    @require_authentication
    def edit_product(product_id):

        product = ProductService.get_product_by_id(product_id)
        if not product:
            return jsonify({"success": False, "message": "Producto no encontrado"}), 404
            
        form = ProductForm(obj=product)
        categories = ProductService.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        if request.method == "POST" and form.validate_on_submit():
            data = {
                "nombre": form.nombre.data,
                "categoria_id": form.categoria_id.data,
                "precio": form.precio.data
            }

            result = ProductService.update_product(product_id, data)

            if result["success"]:
                return redirect(url_for("admin.list_products"))

            return render_template("admin/product_form.html", form=form, error=result["message"])

        return render_template("admin/product_form.html", form=form, product=product)
