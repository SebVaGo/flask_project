from flask import request, jsonify, render_template, redirect, url_for
from app.services.product_service import ProductService
from app.utils.forms.product_form import ProductForm
from app.controllers.base_auth_controller import BaseController
from flask_wtf.csrf import generate_csrf


class ProductController(BaseController):
    @staticmethod
    def list_products():

        user = BaseController.get_authenticated_user()
        if not user:
            return jsonify({"success": False, "message": "No autorizado"}), 401       
         
        """Lista todos los productos en la vista de administración"""
        products = ProductService.get_all_products()
        csrf_token = generate_csrf()  # 🔹 Generar el token CSRF en el backend
        return render_template("admin/products.html", products=products, csrf_token=csrf_token)

    @staticmethod
    def new_product_form():
        user = BaseController.get_authenticated_user()
        if not user:
            return jsonify({"success": False, "message": "No autorizado"}), 401
        
        """Muestra el formulario de creación de productos"""
        form = ProductForm()
        categories = ProductService.get_all_categories()  # Obtener categorías para el select

        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]
        
        return render_template("admin/product_form.html", form=form)

    @staticmethod
    def create_product():
        user = BaseController.get_authenticated_user()
        if not user:
            return jsonify({"success": False, "message": "No autorizado"}), 401
    
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
    def delete_product(product_id):
        """Elimina un producto (solo para usuarios autenticados)"""
        print(f"Intentando eliminar el producto con ID: {product_id}")  # 🔹 DEBUG

        user = ProductController.get_authenticated_user()
        if not user:
            return jsonify({"success": False, "message": "No autorizado"}), 401

        result = ProductService.delete_product(product_id)
        if result["success"]:
            return jsonify({"success": True, "message": "Producto eliminado correctamente"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400
    
    @staticmethod
    def edit_product(product_id):
        """Muestra el formulario de edición de productos"""
        user = BaseController.get_authenticated_user()
        if not user:
            return jsonify({"success": False, "message": "No autorizado"}), 401

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
