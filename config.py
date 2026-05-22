"""Configuración global del sistema."""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'tienda.db')
SCHEMA_PATH = os.path.join(BASE_DIR, 'database', 'schema.sql')
SECRET_KEY = 'clave-academica-cambiar-en-produccion'
