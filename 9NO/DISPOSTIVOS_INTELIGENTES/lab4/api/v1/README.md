# `api/v1/` — Endpoints versión 1

Routers montados bajo el prefijo `/api/v1/...` desde `main.py`.

## Archivos

### `userApi.py`
Router de usuarios (`APIRouter`). Se registra en `main.py` como `/api/v1/users`.

| Método | Ruta relativa | Función |
| --- | --- | --- |
| `POST` | `/` | Crear usuario (`create_user`). Valida email y username únicos |
| `GET` | `/` | Listar todos los usuarios (`get_users`) |
| `GET` | `/{user_id}` | Obtener un usuario por ID (`get_user`) |
| `PUT` | `/{user_id}` | Actualización parcial (`update_user`) con `model_dump(exclude_unset=True)` |
| `DELETE` | `/{user_id}` | Eliminar usuario (`delete_user`); responde `204` |

Usa:
- `get_session` de `db/database.py` (inyección de dependencia)
- modelo `User` de `models/user_model.py`
- esquemas `UserCreate`, `UserUpdate`, `UserResponse` de `schemas/user.py`
