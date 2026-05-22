"""Decoradores para proteger rutas según el rol del usuario."""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_requerido(rol=None):
    """Decorador: redirige a login si no hay sesión, o si el rol no coincide."""
    def decorador(f):
        @wraps(f)
        def envoltura(*args, **kwargs):
            if 'idUsuario' not in session:
                flash('Debes iniciar sesión', 'error')
                return redirect(url_for('auth.login'))
            if rol and session.get('rol') != rol:
                flash('No tienes permiso para acceder aquí', 'error')
                return redirect(url_for('catalogo.ver'))
            return f(*args, **kwargs)
        return envoltura
    return decorador
