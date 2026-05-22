"""Rutas de autenticación: registro, login, logout."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.usuario import Usuario

bp = Blueprint('auth', __name__)


@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre', '').strip()
        email = request.form.get('email', '').strip()
        contrasena = request.form.get('contrasena', '')

        if not nombre or not email or not contrasena:
            flash('Todos los campos son obligatorios', 'error')
            return render_template('registro.html')

        idNuevo = Usuario.registrar(nombre, email, contrasena, rol='cliente')
        if idNuevo:
            flash('Registro exitoso. Ya puedes iniciar sesión.', 'ok')
            return redirect(url_for('auth.login'))
        else:
            flash('Ese email ya está registrado', 'error')
    return render_template('registro.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        contrasena = request.form.get('contrasena', '')
        usuario = Usuario.autenticar(email, contrasena)
        if usuario:
            session['idUsuario'] = usuario.idUsuario
            session['nombre'] = usuario.nombre
            session['rol'] = usuario.rol
            if usuario.rol == 'encargado':
                return redirect(url_for('admin.panel'))
            return redirect(url_for('catalogo.ver'))
        flash('Email o contraseña incorrectos', 'error')
    return render_template('login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
