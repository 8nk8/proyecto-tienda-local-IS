"""Conexión a SQLite. Función única usada por todos los modelos."""
import sqlite3
from config import DB_PATH


def get_connection():
    """Devuelve una conexión a SQLite con row_factory para acceso por nombre."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
