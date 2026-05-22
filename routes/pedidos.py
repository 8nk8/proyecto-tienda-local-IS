"""CU-04: Realizar pedido + ver historial de pedidos del cliente."""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.pedido import Pedido
from models.carrito import Carrito
from routes.utils import login_requerido

bp = Blueprint('pedidos', __name__)


@bp.route('/checkout', methods=['GET', 'POST'])
@login_requerido(rol='cliente')
def checkout():
    carrito = Carrito.obtener_por_cliente(session['idUsuario'])
    if not carrito or not carrito.items:
        flash('Tu carrito está vacío', 'error')
        return redirect(url_for('carrito.ver'))

    if request.method == 'POST':
        direccion = request.form.get('direccion', '').strip()
        metodoPago = request.form.get('metodoPago', '')

        if not direccion:
            flash('La dirección es obligatoria', 'error')
            return render_template('checkout.html', carrito=carrito)
        if metodoPago not in ('tarjeta', 'efectivo'):
            flash('Método de pago inválido', 'error')
            return render_template('checkout.html', carrito=carrito)

        idPedido, mensaje = Pedido.crear_desde_carrito(
            session['idUsuario'], direccion, metodoPago
        )
        if idPedido:
            flash(f'{mensaje}. Tu número de pedido es #{idPedido}', 'ok')
            return redirect(url_for('pedidos.mis_pedidos'))
        else:
            flash(mensaje, 'error')

    return render_template('checkout.html', carrito=carrito)


@bp.route('/mis-pedidos')
@login_requerido(rol='cliente')
def mis_pedidos():
    pedidos = Pedido.listar_por_cliente(session['idUsuario'])
    return render_template('mis_pedidos.html', pedidos=pedidos)
