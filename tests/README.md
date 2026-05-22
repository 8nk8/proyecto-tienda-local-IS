# Tests

Esta carpeta está reservada para los tests unitarios que corresponden
al **Plan de Pruebas** de la Entrega 3 (Sommerville, Cap. 8).

Marco sugerido: `pytest`.

Estructura propuesta:

```
tests/
├── test_producto.py    # Verifica actualizarPrecio, actualizarStock, estaDisponible
├── test_carrito.py     # Verifica agregar_item, quitar_item, calcular_total
└── test_pedido.py      # Verifica crear_desde_carrito, cambiar_estado
```

Cada test debería cubrir:

- Clase de equivalencia normal (valores típicos)
- Valores en el límite (cantidad = 0, stock = 0, precio = 0)
- Valores fuera del rango permitido (cantidades negativas, etc.)
- Casos de excepción (producto agotado, carrito vacío, etc.)

Los casos derivan directamente de los flujos básicos, alternativos y de
excepción documentados en la Entrega 1.
