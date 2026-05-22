"""CU-01: Ver catálogo de productos."""
from flask import Blueprint, render_template, session
from models.producto import Producto
from models.carrito import Carrito
from routes.utils import login_requerido

bp = Blueprint('catalogo', __name__)


@bp.route('/')
def ver():
    """Pantalla de inicio. Muestra el catálogo y el carrito lateral si hay sesión."""
    productos = Producto.listar_todos()
    carrito = None
    if 'idUsuario' in session and session.get('rol') == 'cliente':
        carrito = Carrito.obtener_por_cliente(session['idUsuario'])
    return render_template('catalogo.html', productos=productos, carrito=carrito)
