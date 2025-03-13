from flask import render_template, request, jsonify, flash, redirect, url_for
from app.services.user_service import UserService
from app.utils.forms.user_form import UserForm, UserUpdateForm
from flask_wtf import FlaskForm
from wtforms import HiddenField

class CSRFForm(FlaskForm):
    csrf_token = HiddenField()

def create_user():
    form = UserForm()
    client_types = UserService.get_all_tipe_user()  

    form.tipo_cliente_id.choices = [(tipo.id, tipo.nombre) for tipo in client_types]

    if request.method == "POST" and form.validate_on_submit():
        data = {key: value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}

        resultado = UserService.create_user(data)

        if resultado["success"]:
            flash("Usuario creado correctamente.", "success")
            return jsonify(resultado), 201

        flash(resultado["message"], "danger")
        return jsonify(resultado), 400

    if request.method == "POST":
        errors = {field: messages for field, messages in form.errors.items()}
        return jsonify({"success": False, "errors": errors}), 400

    return render_template("register.html", form=form)

def get_users():
    users = UserService.get_all_users()
    form = CSRFForm()
    return render_template("users.html", users=users, form=form)

def edit_user(user_id):
    user = UserService.get_user_by_id(user_id)
    
    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado."}), 404

    form = UserUpdateForm(obj=user)

    client_types = UserService.get_all_tipe_user()
    form.tipo_cliente_id.choices = [(tipo.id, tipo.nombre) for tipo in client_types]

    if form.validate_on_submit():
        data = {key: value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}
        resultado, status_code = UserService.actualizar_usuario(user_id, data)
        return jsonify(resultado), status_code

    if request.method == "POST":
        return jsonify({"success": False, "errors": form.errors}), 400

    return render_template("edit_user.html", user=user, form=form)

def delete_user(user_id):
    resultado = UserService.delete_user(user_id)
    return jsonify(resultado), 200 if resultado["success"] else 400
