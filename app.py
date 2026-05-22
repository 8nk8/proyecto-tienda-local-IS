"""
Aplicación principal del Sistema de Pedidos en Línea para Tienda Local.

Para correr:
    python app.py

La primera vez crea la base de datos y carga datos de prueba.
"""
import os
from flask import Flask
from config import SECRET_KEY, DB_PATH, SCHEMA_PATH
from database.db import get_connection


def crear_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY

    # Crear la base de datos si no existe
    if not os.path.exists(DB_PATH):
        inicializar_bd()

    # Registrar blueprints
    from routes.auth import bp as auth_bp
    from routes.catalogo import bp as catalogo_bp
    from routes.carrito import bp as carrito_bp
    from routes.pedidos import bp as pedidos_bp
    from routes.admin import bp as admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(catalogo_bp)
    app.register_blueprint(carrito_bp)
    app.register_blueprint(pedidos_bp)
    app.register_blueprint(admin_bp)

    return app


def inicializar_bd():
    """Crea tablas y carga datos de prueba."""
    print('Creando base de datos...')
    conn = get_connection()
    with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
        conn.executescript(f.read())
    conn.close()

    from database.seed import cargar_datos_prueba
    cargar_datos_prueba()
    print('Base de datos lista.')


if __name__ == '__main__':
    app = crear_app()
    app.run(debug=True, port=5000)
