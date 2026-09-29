# `schemas/` — Esquemas Pydantic (API)

Contratos de entrada y salida de la API. No son tablas: validan y serializan JSON.

## Archivos

### `user.py`

| Clase | Uso |
| --- | --- |
| `UserCreate` | Body al crear usuario: `username`, `email`, `password` (obligatorios; `...` = requerido) |
| `UserUpdate` | Body al actualizar: todos los campos opcionales (actualización parcial) |
| `UserResponse` | Lo que devuelve la API: `id`, `username`, `email`, `is_active`, `created_at`. Con `from_attributes = True` puede construirse desde un objeto `User` de SQLModel |

Separar schemas del modelo de BD evita exponer `hashed_password` y permite reglas distintas para create vs update.
