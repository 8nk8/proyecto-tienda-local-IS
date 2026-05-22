"""
Modelo Producto.
Operaciones del diagrama de clases: actualizarPrecio, actualizarStock, estaDisponible.
"""
from database.db import get_connection


class Producto:
    def __init__(self, idProducto, nombre, descripcion, precio, stock):
        self.idProducto = idProducto
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.stock = stock

    @staticmethod
    def _fila_a_producto(fila):
        return Producto(
            fila['idProducto'], fila['nombre'], fila['descripcion'],
            fila['precio'], fila['stock']
        )

    @staticmethod
    def listar_todos():
        """Devuelve todos los productos del catálogo."""
        conn = get_connection()
        try:
            filas = conn.execute("SELECT * FROM Producto ORDER BY nombre").fetchall()
            return [Producto._fila_a_producto(f) for f in filas]
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(idProducto):
        conn = get_connection()
        try:
            fila = conn.execute(
                "SELECT * FROM Producto WHERE idProducto = ?", (idProducto,)
            ).fetchone()
            return Producto._fila_a_producto(fila) if fila else None
        finally:
            conn.close()

    def esta_disponible(self, cantidad):
        """Verifica si hay stock suficiente para la cantidad solicitada."""
        return self.stock >= cantidad

    def actualizar_precio(self, nuevo_precio):
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo")
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE Producto SET precio = ? WHERE idProducto = ?",
                (nuevo_precio, self.idProducto)
            )
            conn.commit()
            self.precio = nuevo_precio
        finally:
            conn.close()

    def actualizar_stock(self, nueva_cantidad):
        if nueva_cantidad < 0:
            raise ValueError("El stock no puede ser negativo")
        conn = get_connection()
        try:
            conn.execute(
                "UPDATE Producto SET stock = ? WHERE idProducto = ?",
                (nueva_cantidad, self.idProducto)
            )
            conn.commit()
            self.stock = nueva_cantidad
        finally:
            conn.close()
