"""
Modelo Usuario: unifica las clases de diseño Cliente y Encargado.

Simplificación consciente respecto al diagrama de clases (Entrega 2):
ambas clases compartían atributos (idUsuario, nombre, email, contraseña)
y se diferenciaban solo en codigoEmpleado vs lista de direcciones.
La distinción de comportamiento se maneja con el campo 'rol'.
"""
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_connection


class Usuario:
    def __init__(self, idUsuario, nombre, email, rol):
        self.idUsuario = idUsuario
        self.nombre = nombre
        self.email = email
        self.rol = rol

    @staticmethod
    def registrar(nombre, email, contrasena, rol='cliente'):
        """Crea un nuevo usuario. Devuelve el id o None si el email ya existe."""
        conn = get_connection()
        try:
            hash_pwd = generate_password_hash(contrasena)
            cursor = conn.execute(
                "INSERT INTO Usuario (nombre, email, contrasena, rol) VALUES (?, ?, ?, ?)",
                (nombre, email, hash_pwd, rol)
            )
            id_nuevo = cursor.lastrowid
            # Si es cliente, crearle un carrito vacío de inmediato
            if rol == 'cliente':
                conn.execute(
                    "INSERT INTO Carrito (idCliente, fechaCreacion) VALUES (?, datetime('now'))",
                    (id_nuevo,)
                )
            conn.commit()
            return id_nuevo
        except Exception:
            return None
        finally:
            conn.close()

    @staticmethod
    def autenticar(email, contrasena):
        """Verifica credenciales. Devuelve un Usuario o None."""
        conn = get_connection()
        try:
            fila = conn.execute(
                "SELECT * FROM Usuario WHERE email = ?", (email,)
            ).fetchone()
            if fila and check_password_hash(fila['contrasena'], contrasena):
                return Usuario(fila['idUsuario'], fila['nombre'], fila['email'], fila['rol'])
            return None
        finally:
            conn.close()

    @staticmethod
    def buscar_por_id(idUsuario):
        conn = get_connection()
        try:
            fila = conn.execute(
                "SELECT * FROM Usuario WHERE idUsuario = ?", (idUsuario,)
            ).fetchone()
            if fila:
                return Usuario(fila['idUsuario'], fila['nombre'], fila['email'], fila['rol'])
            return None
        finally:
            conn.close()
