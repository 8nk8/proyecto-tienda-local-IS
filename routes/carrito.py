"""CU-02 Agregar producto al carrito, CU-03 Quitar producto del carrito."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.carrito import Carrito
from routes.utils import login_requerido

bp = Blueprint('carrito', __name__)


@bp.route('/carrito')
@login_requerido(rol='cliente')
def ver():
    carrito = Carrito.obtener_por_cliente(session['idUsuario'])
    return render_template('carrito.html', carrito=carrito)


@bp.route('/carrito/agregar/<int:idProducto>', methods=['POST'])
@login_requerido(rol='cliente')
def agregar(idProducto):
    cantidad = int(request.form.get('cantidad', 1))
    carrito = Carrito.obtener_por_cliente(session['idUsuario'])
    ok, mensaje = carrito.agregar_item(idProducto, cantidad)
    flash(mensaje, 'ok' if ok else 'error')
    return redirect(request.referrer or url_for('catalogo.ver'))


@bp.route('/carrito/quitar/<int:idProducto>', methods=['POST'])
@login_requerido(rol='cliente')
def quitar(idProducto):
    carrito = Carrito.obtener_por_cliente(session['idUsuario'])
    carrito.quitar_item(idProducto)
    flash('Producto eliminado del carrito', 'ok')
    return redirect(url_for('carrito.ver'))


@bp.route('/carrito/actualizar/<int:idProducto>', methods=['POST'])
@login_requerido(rol='cliente')
def actualizar(idProducto):
    nueva = int(request.form.get('cantidad', 1))
    carrito = Carrito.obtener_por_cliente(session['idUsuario'])
    ok, mensaje = carrito.actualizar_cantidad(idProducto, nueva)
    flash(mensaje, 'ok' if ok else 'error')
    return redirect(url_for('carrito.ver'))
