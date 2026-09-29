# `db/` — Acceso a base de datos

Configuración del motor SQLModel/SQLAlchemy y obtención de sesiones.

## Archivos

### `database.py`
| Elemento | Qué hace |
| --- | --- |
| `load_dotenv()` | Carga variables desde `.env` en la raíz del proyecto |
| `DATABASE_URL` | URL de conexión; por defecto `sqlite:///./mikedb.db` |
| `engine` | Motor SQLAlchemy/SQLModel; en SQLite usa `check_same_thread=False` |
| `create_db_and_tables()` | Crea las tablas definidas en los modelos (`SQLModel.metadata.create_all`) |
| `get_session()` | Generador de `Session` para inyección con `Depends` en los endpoints |

Se usa en el `lifespan` de `main.py` (crear tablas al arrancar) y en los routers (sesiones por petición).
