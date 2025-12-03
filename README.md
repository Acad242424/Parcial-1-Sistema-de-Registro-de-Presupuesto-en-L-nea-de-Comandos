# Budget CLI

Aplicación de línea de comandos para gestionar artículos en un sistema de registro de presupuesto.

## Requisitos
- Python 3.8+
- Instalar dependencias:
```
pip install -r requirements.txt
```

## Archivos principales
- `app.py` - Interfaz principal (menú) y validación de entradas.
- `storage.py` - Módulo que maneja la base de datos SQLite (`budget.db`).

## Uso
Desde el directorio del proyecto:
```
python app.py
```
Se mostrará un menú interactivo para listar, crear, buscar, editar y eliminar artículos.

## Estructura de datos
Cada artículo contiene:
- `name` (texto)
- `category` (texto)
- `quantity` (entero)
- `unit_price` (decimal)
- `description` (texto opcional)
- timestamps `created_at` y `updated_at`

## Notas
- La base de datos `budget.db` se crea automáticamente en el directorio de ejecución.
- El proyecto incluye validación básica de entradas y mensajes amigables.
