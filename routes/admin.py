"""CU-05: Consultar pedidos del día y actualizar estados (vista del encargado)."""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models.pedido import Pedido
from routes.utils import login_requerido

bp = Blueprint('admin', __name__)


@bp.route('/admin')
@login_requerido(rol='encargado')
def panel():
    """Muestra pedidos del día con métricas básicas."""
    fecha = request.args.get('fecha')  # opcional, formato YYYY-MM-DD
    pedidos = Pedido.listar_por_fecha(fecha)

    total_ventas = sum(p.total for p in pedidos)
    pendientes = sum(1 for p in pedidos if p.estado == 'pendiente')

    return render_template(
        'admin.html', pedidos=pedidos, fecha=fecha,
        total_ventas=total_ventas, pendientes=pendientes,
        total_pedidos=len(pedidos)
    )


@bp.route('/admin/pedido/<int:idPedido>/estado', methods=['POST'])
@login_requerido(rol='encargado')
def cambiar_estado(idPedido):
    nuevo_estado = request.form.get('estado', '')
    if Pedido.cambiar_estado(idPedido, nuevo_estado):
        flash(f'Pedido #{idPedido} actualizado a "{nuevo_estado}"', 'ok')
    else:
        flash('No se pudo actualizar el pedido', 'error')
    return redirect(url_for('admin.panel'))
