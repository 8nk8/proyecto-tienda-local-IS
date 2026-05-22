# Sistema de Pedidos en Línea para Tienda Local

Implementación funcional simplificada del proyecto de Ingeniería de Software.
Corresponde a la **Entrega 3: Producto Final**: código fuente del sistema
(Jacobson, Cap. 10).

## Stack

- **Python 3.9+** con **Flask** (servidor web)
- **SQLite** (base de datos, archivo único)
- **Jinja2** (plantillas HTML)
- **Werkzeug** (hashing de contraseñas)

## Instalación

```bash
# 1. Clonar o descomprimir el proyecto
cd tienda_local

# 2. (Recomendado) crear un entorno virtual
python -m venv venv
source venv/bin/activate          # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Correr la aplicación
python app.py
```

La primera vez que se ejecuta, se crea automáticamente la base de datos
`database/tienda.db` con datos de prueba.

Luego abrir en el navegador: <http://localhost:5000>

## Usuarios de prueba

| Rol       | Email                | Contraseña   |
| --------- | -------------------- | ------------ |
| Cliente   | cliente@tienda.com   | cliente123   |
| Encargado | encargado@tienda.com | encargado123 |

## Casos de uso implementados

| ID    | Caso de uso                       | Ruta                    |
| ----- | --------------------------------- | ----------------------- |
| CU-01 | Ver catálogo                      | `/`                     |
| CU-02 | Agregar producto al carrito       | `POST /carrito/agregar` |
| CU-03 | Quitar producto del carrito       | `POST /carrito/quitar`  |
| CU-04 | Realizar pedido                   | `/checkout`             |
| CU-05 | Consultar pedidos del día (admin) | `/admin`                |

## Estructura del proyecto

```
tienda_local/
├── app.py                # Punto de entrada Flask
├── config.py             # Configuración
├── requirements.txt
├── database/
│   ├── schema.sql        # DDL de las tablas
│   ├── seed.py           # Datos de prueba
│   └── db.py             # Helper de conexión
├── models/               # Clases de diseño (Jacobson 10.5.4)
│   ├── usuario.py
│   ├── producto.py
│   ├── carrito.py
│   └── pedido.py
├── routes/               # Controladores HTTP
│   ├── auth.py
│   ├── catalogo.py
│   ├── carrito.py
│   ├── pedidos.py
│   └── admin.py
├── templates/            # Plantillas Jinja2 
├── static/style.css
└── tests/                # 
```

## Para resetear la base de datos

```bash
rm database/tienda.db
python app.py
```
