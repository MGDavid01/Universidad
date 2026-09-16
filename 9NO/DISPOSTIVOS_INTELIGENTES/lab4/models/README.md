# `models/` — Modelos de base de datos

Definición de tablas con SQLModel (`table=True`). Representan cómo se guardan los datos en la BD.

## Archivos

### `user_model.py`
Modelo `User` → tabla `users`.

| Campo | Tipo / notas |
| --- | --- |
| `id` | PK opcional en Python; la BD la genera al insertar |
| `username` | Único, indexado, 3–50 caracteres |
| `email` | Único, indexado |
| `hashed_password` | Contraseña almacenada (debe ir hasheada en producción) |
| `is_active` | `bool`, por defecto `True` |
| `created_at` | Fecha/hora de creación (`datetime.utcnow`) |

Los endpoints de `api/v1/userApi.py` leen y escriben sobre esta clase.
