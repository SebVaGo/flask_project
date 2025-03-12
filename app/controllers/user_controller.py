from flask import render_template, request, jsonify, flash, redirect, url_for
from app.services.user_service import UserService
from app.utils.forms.user_form import UserForm
from app.utils.forms.user_form import UserUpdateForm
from flask_wtf.csrf import validate_csrf
from wtforms import HiddenField
from flask_wtf import FlaskForm

class CSRFForm(FlaskForm):
    csrf_token = HiddenField()


def create_user():
    form = UserForm()
    
    if request.method == "POST":
        csrf_token = request.headers.get('X-CSRFToken')
        
        form.csrf_token.data = csrf_token
        
        if form.validate_on_submit():
            validated_data = form.data.copy()  
            validated_data.pop("csrf_token", None)  
            validated_data.pop("submit", None) 
            
            print("Datos enviados al servicio:", validated_data)  
            
            response, status = UserService.create_user(validated_data)
            
            if status == 201:
                return jsonify({"success": True, "message": "Usuario registrado exitosamente."}), 201
            return jsonify({"success": False, "message": response.get("message", "Error al registrar el usuario.")}), 400
        
        return jsonify({"success": False, "errors": form.errors}), 400
    
    return render_template("register.html", form=form)

def get_users():
    users = UserService.get_all_users()
    form = CSRFForm()  

    return render_template("users.html", users=users, form=form)

def edit_user(user_id):
    """ Muestra la página de edición del usuario y procesa la actualización """
    
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({"success": False, "message": "Usuario no encontrado"}), 404

    form = UserUpdateForm(obj=user) 

    if request.method == "POST":
        try:
            
            csrf_token = request.headers.get("X-CSRFToken")
            form.csrf_token.data = csrf_token  

            if form.validate_on_submit(): 
                data = request.form.to_dict()
                resultado = UserService.actualizar_usuario(user_id, data)

                if resultado["success"]:
                    return jsonify({"success": True, "message": "Usuario actualizado correctamente."}), 200
                else:
                    return jsonify({"success": False, "message": resultado["message"]}), 400
            else:
                return jsonify({"success": False, "message": "Error de validación.", "errors": form.errors}), 400
        except Exception as e:
            return jsonify({"success": False, "message": f"Error interno: {str(e)}"}), 500

    return render_template("edit_user.html", user=user, form=form)

def delete_user(user_id):
    try:
        csrf_token = request.headers.get("X-CSRFToken") 
        validate_csrf(csrf_token)  

        resultado = UserService.delete_user(user_id)  

        if resultado["success"]:
            return jsonify({"success": True, "message": "Usuario eliminado correctamente."}), 200
        else:
            return jsonify({"success": False, "message": resultado["message"]}), 400
    except Exception as e:
        return jsonify({"success": False, "message": f"Error interno: {str(e)}"}), 500
