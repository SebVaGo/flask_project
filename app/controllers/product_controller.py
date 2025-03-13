from flask import request, jsonify
from flask_wtf.csrf import generate_csrf
from app.services.product_service import ProductService
from app.utils.forms.product_form import ProductForm
from app.controllers.base_controller import BaseController

product_service = ProductService()

class ProductController(BaseController):

    def __init__(self):
        super().__init__()


    def list_products(self):
        products = product_service.get_all_products()
        csrf_token = generate_csrf()
        return self.render("admin/products.html", products=products, csrf_token=csrf_token)

    def new_product_form(self):
        form = ProductForm()
        categories = product_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]
        csrf_token = generate_csrf()
        return self.render("admin/product_form.html", form=form, csrf_token=csrf_token)

    def create_product(self):
        form = ProductForm()
        categories = product_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        errors = self.validate_form(form)
        if errors:
            csrf_token = generate_csrf()
            return self.render("admin/product_form.html", form=form, errors=errors, csrf_token=csrf_token)

        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        result = product_service.create_product(data)

        if result["success"]:
            return jsonify({"success": True, "message": "Producto creado correctamente"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400

    def delete_product(self, product_id):
        result = product_service.delete_product(product_id)

        if result["success"]:
            return jsonify({"success": True, "message": "Producto eliminado correctamente"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400

    def edit_product(self, product_id):
        product = product_service.get_product_by_id(product_id)
        if not product:
            return jsonify({"success": False, "message": "Producto no encontrado"}), 404

        form = ProductForm(obj=product)
        categories = product_service.get_all_categories()
        form.categoria_id.choices = [(c.id, c.nombre) for c in categories]

        if request.method == "GET":
            csrf_token = generate_csrf()
            return self.render("admin/product_form.html", form=form, product=product, csrf_token=csrf_token)

        errors = self.validate_form(form)
        if errors:
            return jsonify({"success": False, "errors": errors}), 400

        data = {
            "nombre": form.nombre.data,
            "categoria_id": form.categoria_id.data,
            "precio": form.precio.data
        }

        result = product_service.update_product(product_id, data)

        if result["success"]:
            return jsonify({"success": True, "message": "Producto actualizado correctamente"}), 200

        return jsonify({"success": False, "message": result["message"]}), 400
