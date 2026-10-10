# `api/` — Capa HTTP

Contiene los routers de FastAPI agrupados por versión de la API.

## Contenido

| Ruta | Descripción |
| --- | --- |
| `v1/` | Primera versión de la API (`/api/v1/...`) |

Cada versión tiene sus propios endpoints para poder evolucionar sin romper clientes antiguos.
