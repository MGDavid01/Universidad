# Lab 4 — FastAPI + SQLModel

API REST de usuarios con FastAPI, SQLModel y base de datos (SQLite local o PostgreSQL con Podman/Compose).

## Estructura del proyecto

| Carpeta / archivo | Rol |
| --- | --- |
| `main.py` | Punto de entrada: crea la app FastAPI, ciclo de vida (startup/shutdown), CORS y routers |
| `compose.yml` | Orquestación de PostgreSQL 15 para desarrollo con contenedores |
| `.env` | Variables de entorno (p. ej. `DATABASE_URL`). No versionar secretos reales |
| `mikedb.db` | Base SQLite generada en local si no usas PostgreSQL |
| `pyrightconfig.json` | Configuración del analizador de tipos Pyright |
| `api/` | Endpoints HTTP versionados |
| `core/` | Utilidades transversales (CORS, hashing de contraseñas) |
| `db/` | Conexión al motor y sesiones de base de datos |
| `models/` | Modelos SQLModel (tablas) |
| `schemas/` | Esquemas Pydantic de entrada/salida de la API |

## Archivos en la raíz

### `main.py`
- Define el `lifespan` que crea tablas al arrancar.
- Instancia `FastAPI`, aplica CORS e incluye el router de usuarios en `/api/v1/users`.
- Expone `GET /` (bienvenida) y `GET /health` (salud del servicio).

### `compose.yml`
Quedó de cuando este lab tenía su propio Postgres. El stack compartido está en la raíz de `Universidad` (`docker compose up -d postgres`): contenedor `uni-postgres`, base `mikedb` o `lab4`.

### `.env`
Define la URL de conexión. Ejemplo comentado para Postgres; si no hay valor, `db/database.py` usa SQLite (`sqlite:///./mikedb.db`).

### `pyrightconfig.json`
Ajustes de tipado estático para el IDE / Pyright.

### `sys`
Documento PostScript (no forma parte del código de la API).

## Cómo arrancar (resumen)

```bash
# Opcional: PostgreSQL compartido (desde la raíz de Universidad)
docker compose up -d postgres
# o: podman compose up -d postgres

# API (desde el entorno Dev)
uvicorn main:app --reload
```

Documentación interactiva: `http://127.0.0.1:8000/docs`
