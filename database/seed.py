"""Carga datos de prueba: productos de abarrotes y un usuario encargado."""
from werkzeug.security import generate_password_hash
from database.db import get_connection


PRODUCTOS = [
    ("Leche entera 1L", "Leche pasteurizada en envase Tetra Pak", 28.50, 30),
    ("Pan blanco grande", "Pan de caja blanco, 680g", 45.00, 20),
    ("Huevo San Juan 18 pz", "Cartón con 18 huevos blancos", 65.00, 25),
    ("Arroz superior 1kg", "Arroz blanco grano largo", 32.00, 40),
    ("Frijol negro 1kg", "Frijol negro seleccionado", 38.50, 35),
    ("Aceite vegetal 1L", "Aceite vegetal puro", 52.00, 18),
    ("Azúcar estándar 1kg", "Azúcar refinada", 28.00, 50),
    ("Sal de mesa 1kg", "Sal yodada", 15.00, 60),
    ("Atún en agua 140g", "Lata de atún en agua", 22.50, 45),
    ("Refresco cola 2L", "Refresco sabor cola", 35.00, 30),
    ("Papel higiénico 4 rollos", "Papel higiénico doble hoja", 48.00, 22),
    ("Detergente líquido 1L", "Detergente para ropa", 58.00, 15),
]


def cargar_datos_prueba():
    conn = get_connection()
    try:
        # Crear usuario encargado
        conn.execute(
            "INSERT INTO Usuario (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)",
            ("Encargado Demo", "encargado@tienda.com",
             generate_password_hash("encargado123"), "encargado")
        )

        # Crear cliente de prueba con carrito
        cursor = conn.execute(
            "INSERT INTO Usuario (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)",
            ("Cliente Demo", "cliente@tienda.com",
             generate_password_hash("cliente123"), "cliente")
        )
        idCliente = cursor.lastrowid
        conn.execute(
            "INSERT INTO Carrito (idCliente, fechaCreacion) VALUES (?, datetime('now'))",
            (idCliente,)
        )

        # Cargar productos
        for nombre, desc, precio, stock in PRODUCTOS:
            conn.execute(
                "INSERT INTO Producto (nombre, descripcion, precio, stock) VALUES (?, ?, ?, ?)",
                (nombre, desc, precio, stock)
            )

        conn.commit()
        print(f"  - {len(PRODUCTOS)} productos cargados")
        print(f"  - Usuario encargado: encargado@tienda.com / encargado123")
        print(f"  - Usuario cliente:   cliente@tienda.com / cliente123")
    finally:
        conn.close()


if __name__ == '__main__':
    cargar_datos_prueba()
