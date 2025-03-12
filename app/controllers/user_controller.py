from flask import render_template, request, jsonify, flash, redirect, url_for
from app.services.user_service import UserService
from app.utils.forms.user_form import UserForm, UserUpdateForm
from flask_wtf import FlaskForm
from wtforms import HiddenField

class CSRFForm(FlaskForm):
    csrf_token = HiddenField()

def create_user():
    """Maneja la creación de usuarios"""
    form = UserForm()
    
    if request.method == "POST" and form.validate_on_submit():
        data = {key: value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}
        resultado = UserService.create_user(data)

        if resultado["success"]:
            flash("Usuario creado correctamente.", "success")
            return jsonify(resultado), 201

        return jsonify(resultado), 400

    return render_template("register.html", form=form)

def get_users():
    """Muestra la lista de usuarios"""
    users = UserService.get_all_users()
    form = CSRFForm()
    return render_template("users.html", users=users, form=form)

def edit_user(user_id):
    """Muestra la página de edición del usuario y maneja la actualización"""
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    form = UserUpdateForm(obj=user)

    if request.method == "POST" and form.validate_on_submit():
        data = {key: value for key, value in form.data.items() if key not in ["submit", "csrf_token"]}
        resultado = UserService.actualizar_usuario(user_id, data)

        return jsonify(resultado), 200 if resultado["success"] else 400

    return render_template("edit_user.html", user=user, form=form)

def delete_user(user_id):
    """Elimina un usuario"""
    resultado = UserService.delete_user(user_id)
    return jsonify(resultado), 200 if resultado["success"] else 400
