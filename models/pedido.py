"""
Modelo Pedido y DetallePedido.
DETALLE_PEDIDO almacena precioUnitario histórico para proteger
la integridad financiera ante cambios en el catálogo
(decisión justificada en la sección 4.2 de la Entrega 2).
"""
from database.db import get_connection
from models.carrito import Carrito


class DetallePedido:
    def __init__(self, idDetalle, idProducto, nombre, cantidad, precioUnitario):
        self.idDetalle = idDetalle
        self.idProducto = idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precioUnitario = precioUnitario

    def subtotal(self):
        return self.cantidad * self.precioUnitario


class Pedido:
    def __init__(self, idPedido, idCliente, nombreCliente, fecha, estado,
                 direccionEntrega, metodoPago, total, detalles=None):
        self.idPedido = idPedido
        self.idCliente = idCliente
        self.nombreCliente = nombreCliente
        self.fecha = fecha
        self.estado = estado
        self.direccionEntrega = direccionEntrega
        self.metodoPago = metodoPago
        self.total = total
        self.detalles = detalles or []

    @staticmethod
    def crear_desde_carrito(idCliente, direccion, metodoPago):
        """
        CU-04 Realizar Pedido. Verifica stock, descuenta inventario,
        crea el pedido, copia detalles con precio histórico y vacía el carrito.
        Devuelve (idPedido, mensaje) o (None, error).
        """
        carrito = Carrito.obtener_por_cliente(idCliente)
        if not carrito or not carrito.items:
            return None, "El carrito está vacío"

        conn = get_connection()
        try:
            # Verificar stock de TODOS los items antes de proceder
            for item in carrito.items:
                fila = conn.execute(
                    "SELECT stock FROM Producto WHERE idProducto = ?",
                    (item.idProducto,)
                ).fetchone()
                if fila['stock'] < item.cantidad:
                    return None, f"Stock insuficiente para {item.nombre}"

            total = carrito.calcular_total()

            # Crear el pedido
            cursor = conn.execute("""
                INSERT INTO Pedido (idCliente, fecha, estado, direccionEntrega, metodoPago, total)
                VALUES (?, datetime('now'), 'pendiente', ?, ?, ?)
            """, (idCliente, direccion, metodoPago, total))
            idPedido = cursor.lastrowid

            # Copiar items a DetallePedido con precio histórico y descontar stock
            for item in carrito.items:
                conn.execute("""
                    INSERT INTO DetallePedido (idPedido, idProducto, cantidad, precioUnitario)
                    VALUES (?, ?, ?, ?)
                """, (idPedido, item.idProducto, item.cantidad, item.precioUnitario))

                conn.execute(
                    "UPDATE Producto SET stock = stock - ? WHERE idProducto = ?",
                    (item.cantidad, item.idProducto)
                )

            # Vaciar el carrito
            conn.execute("DELETE FROM ItemCarrito WHERE idCarrito = ?", (carrito.idCarrito,))
            conn.commit()
            return idPedido, "Pedido registrado correctamente"
        except Exception as e:
            conn.rollback()
            return None, f"Error al crear pedido: {e}"
        finally:
            conn.close()

    @staticmethod
    def listar_por_cliente(idCliente):
        conn = get_connection()
        try:
            filas = conn.execute("""
                SELECT p.*, u.nombre AS nombreCliente
                FROM Pedido p JOIN Usuario u ON p.idCliente = u.idUsuario
                WHERE p.idCliente = ?
                ORDER BY p.fecha DESC
            """, (idCliente,)).fetchall()
            return [Pedido._con_detalles(f, conn) for f in filas]
        finally:
            conn.close()

    @staticmethod
    def listar_por_fecha(fecha):
        """CU-05 Consultar pedidos del día. Si fecha es None, devuelve los de hoy."""
        conn = get_connection()
        try:
            if fecha:
                query = """
                    SELECT p.*, u.nombre AS nombreCliente
                    FROM Pedido p JOIN Usuario u ON p.idCliente = u.idUsuario
                    WHERE date(p.fecha) = ?
                    ORDER BY p.fecha DESC
                """
                filas = conn.execute(query, (fecha,)).fetchall()
            else:
                query = """
                    SELECT p.*, u.nombre AS nombreCliente
                    FROM Pedido p JOIN Usuario u ON p.idCliente = u.idUsuario
                    WHERE date(p.fecha) = date('now')
                    ORDER BY p.fecha DESC
                """
                filas = conn.execute(query).fetchall()
            return [Pedido._con_detalles(f, conn) for f in filas]
        finally:
            conn.close()

    @staticmethod
    def _con_detalles(fila, conn):
        detalles_filas = conn.execute("""
            SELECT d.idDetalle, d.idProducto, d.cantidad, d.precioUnitario, p.nombre
            FROM DetallePedido d JOIN Producto p ON d.idProducto = p.idProducto
            WHERE d.idPedido = ?
        """, (fila['idPedido'],)).fetchall()

        detalles = [
            DetallePedido(f['idDetalle'], f['idProducto'], f['nombre'],
                          f['cantidad'], f['precioUnitario'])
            for f in detalles_filas
        ]
        return Pedido(
            fila['idPedido'], fila['idCliente'], fila['nombreCliente'],
            fila['fecha'], fila['estado'], fila['direccionEntrega'],
            fila['metodoPago'], fila['total'], detalles
        )

    @staticmethod
    def cambiar_estado(idPedido, nuevo_estado):
        if nuevo_estado not in ('pendiente', 'en camino', 'entregado'):
            return False
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE Pedido SET estado = ? WHERE idPedido = ?",
                (nuevo_estado, idPedido)
            )
            conn.commit()
            return True
        finally:
            conn.close()
