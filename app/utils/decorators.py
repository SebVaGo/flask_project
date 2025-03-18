# app/utils/decorators.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import login_required, current_user
from app.utils.db_session_manager import AltDBSessionManager
from app.config import db
from app.models.user_model import UserModel


def login_required_for_all_methods(cls):

    for attr_name in dir(cls):
        if not attr_name.startswith('__'): 
            attr = getattr(cls, attr_name)
            if callable(attr): 
                decorated = login_required(attr)
                
                @wraps(decorated)
                def session_handler(*args, **kwargs):
                    if current_user.is_authenticated:
                        try:
                            user = db.session.merge(current_user)
                            db.session.refresh(user)
                        except:
                            db.session.rollback()
                    return decorated(*args, **kwargs)
                
                setattr(cls, attr_name, session_handler)
    return cls


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Acceso denegado - Debe iniciar sesión', 'danger')
            return redirect(url_for('auth.login'))

        try:
            with AltDBSessionManager() as session:
                user = session.query(UserModel).filter(UserModel.id == current_user.id).first()
                
                if not user or user.tipo_cliente_id != 1:
                    flash('Acceso denegado - Se requieren permisos de administrador', 'danger')
                    return redirect(url_for('auth.login'))
        except Exception as e:
            flash('Error de verificación - Intente nuevamente', 'danger')
            return redirect(url_for('auth.login'))
            
        return f(*args, **kwargs)
    return decorated_function


def admin_required_for_all_methods(cls):

    for attr_name in dir(cls):
        if not attr_name.startswith('__'):  
            attr = getattr(cls, attr_name)
            if callable(attr):  
                setattr(cls, attr_name, admin_required(attr))
    return cls


def admin_and_login_required_for_all_methods(cls):

    for attr_name in dir(cls):
        if not attr_name.startswith('__'):  
            attr = getattr(cls, attr_name)
            if callable(attr):  
                decorated_method = admin_required(login_required_for_all_methods(attr))
                setattr(cls, attr_name, decorated_method)
    return cls