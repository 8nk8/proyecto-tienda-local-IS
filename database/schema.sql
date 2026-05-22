-- Esquema de base de datos del sistema de pedidos
-- Traza al diagrama Entidad-Relación de la Entrega 2 (Figura 10).
-- Simplificación: Cliente y Encargado se unifican en Usuario (campo rol).
-- Dirección se almacena como texto plano en Pedido (no como tabla aparte).

CREATE TABLE IF NOT EXISTS Usuario (
    idUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    contrasena TEXT NOT NULL,
    rol TEXT NOT NULL CHECK(rol IN ('cliente', 'encargado'))
);

CREATE TABLE IF NOT EXISTS Producto (
    idProducto INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    descripcion TEXT,
    precio REAL NOT NULL CHECK(precio >= 0),
    stock INTEGER NOT NULL CHECK(stock >= 0)
);

CREATE TABLE IF NOT EXISTS Carrito (
    idCarrito INTEGER PRIMARY KEY AUTOINCREMENT,
    idCliente INTEGER NOT NULL UNIQUE,
    fechaCreacion TEXT NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES Usuario(idUsuario)
);

CREATE TABLE IF NOT EXISTS ItemCarrito (
    idItemCarrito INTEGER PRIMARY KEY AUTOINCREMENT,
    idCarrito INTEGER NOT NULL,
    idProducto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK(cantidad > 0),
    precioUnitario REAL NOT NULL,
    FOREIGN KEY (idCarrito) REFERENCES Carrito(idCarrito) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto),
    UNIQUE(idCarrito, idProducto)
);

CREATE TABLE IF NOT EXISTS Pedido (
    idPedido INTEGER PRIMARY KEY AUTOINCREMENT,
    idCliente INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    estado TEXT NOT NULL CHECK(estado IN ('pendiente', 'en camino', 'entregado')),
    direccionEntrega TEXT NOT NULL,
    metodoPago TEXT NOT NULL CHECK(metodoPago IN ('tarjeta', 'efectivo')),
    total REAL NOT NULL,
    FOREIGN KEY (idCliente) REFERENCES Usuario(idUsuario)
);

CREATE TABLE IF NOT EXISTS DetallePedido (
    idDetalle INTEGER PRIMARY KEY AUTOINCREMENT,
    idPedido INTEGER NOT NULL,
    idProducto INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    precioUnitario REAL NOT NULL,  -- Precio histórico al momento de la compra
    FOREIGN KEY (idPedido) REFERENCES Pedido(idPedido) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES Producto(idProducto)
);
