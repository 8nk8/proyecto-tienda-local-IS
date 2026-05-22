"""
Modelo Carrito y ItemCarrito.
Se agrupan en un mismo archivo porque siempre se usan juntos
(ItemCarrito no tiene sentido fuera de un Carrito).
"""
from database.db import get_connection
from models.producto import Producto


class ItemCarrito:
    def __init__(self, idItemCarrito, idProducto, nombre, cantidad, precioUnitario):
        self.idItemCarrito = idItemCarrito
        self.idProducto = idProducto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precioUnitario = precioUnitario

    def subtotal(self):
        return self.cantidad * self.precioUnitario


class Carrito:
    def __init__(self, idCarrito, idCliente, items):
        self.idCarrito = idCarrito
        self.idCliente = idCliente
        self.items = items

    @staticmethod
    def obtener_por_cliente(idCliente):
        """Recupera el carrito activo del cliente con todos sus ítems."""
        conn = get_connection()
        try:
            fila_c = conn.execute(
                "SELECT * FROM Carrito WHERE idCliente = ?", (idCliente,)
            ).fetchone()
            if not fila_c:
                return None

            filas_items = conn.execute("""
                SELECT i.idItemCarrito, i.idProducto, i.cantidad, i.precioUnitario, p.nombre
                FROM ItemCarrito i
                JOIN Producto p ON i.idProducto = p.idProducto
                WHERE i.idCarrito = ?
            """, (fila_c['idCarrito'],)).fetchall()

            items = [
                ItemCarrito(f['idItemCarrito'], f['idProducto'], f['nombre'],
                            f['cantidad'], f['precioUnitario'])
                for f in filas_items
            ]
            return Carrito(fila_c['idCarrito'], fila_c['idCliente'], items)
        finally:
            conn.close()

    def agregar_item(self, idProducto, cantidad):
        """
        Agrega un producto al carrito. Si ya existe, suma la cantidad.
        Verifica stock antes de agregar. Devuelve (ok, mensaje).
        """
        producto = Producto.buscar_por_id(idProducto)
        if not producto:
            return False, "Producto no encontrado"
        if producto.stock == 0:
            return False, "Producto agotado"

        conn = get_connection()
        try:
            existente = conn.execute(
                "SELECT idItemCarrito, cantidad FROM ItemCarrito WHERE idCarrito = ? AND idProducto = ?",
                (self.idCarrito, idProducto)
            ).fetchone()

            nueva_cantidad = (existente['cantidad'] if existente else 0) + cantidad
            if nueva_cantidad > producto.stock:
                return False, "No hay suficiente stock disponible"

            if existente:
                conn.execute(
                    "UPDATE ItemCarrito SET cantidad = ? WHERE idItemCarrito = ?",
                    (nueva_cantidad, existente['idItemCarrito'])
                )
            else:
                conn.execute(
                    "INSERT INTO ItemCarrito (idCarrito, idProducto, cantidad, precioUnitario) VALUES (?, ?, ?, ?)",
                    (self.idCarrito, idProducto, cantidad, producto.precio)
                )
            conn.commit()
            return True, "Producto agregado al carrito"
        finally:
            conn.close()

    def quitar_item(self, idProducto):
        """Elimina por completo un producto del carrito."""
        conn = get_connection()
        try:
            conn.execute(
                "DELETE FROM ItemCarrito WHERE idCarrito = ? AND idProducto = ?",
                (self.idCarrito, idProducto)
            )
            conn.commit()
        finally:
            conn.close()

    def actualizar_cantidad(self, idProducto, nueva_cantidad):
        """Si nueva_cantidad es 0 o menor, elimina el ítem."""
        if nueva_cantidad <= 0:
            self.quitar_item(idProducto)
            return True, "Producto eliminado"

        producto = Producto.buscar_por_id(idProducto)
        if nueva_cantidad > producto.stock:
            return False, "No hay suficiente stock"

        conn = get_connection()
        try:
            conn.execute(
                "UPDATE ItemCarrito SET cantidad = ? WHERE idCarrito = ? AND idProducto = ?",
                (nueva_cantidad, self.idCarrito, idProducto)
            )
            conn.commit()
            return True, "Cantidad actualizada"
        finally:
            conn.close()

    def calcular_total(self):
        return sum(item.subtotal() for item in self.items)

    def vaciar(self):
        conn = get_connection()
        try:
            conn.execute("DELETE FROM ItemCarrito WHERE idCarrito = ?", (self.idCarrito,))
            conn.commit()
        finally:
            conn.close()
