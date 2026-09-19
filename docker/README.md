# Bases de datos compartidas

Un contenedor por motor para todo el repo `Universidad`. No levantes un MySQL/Postgres nuevo en cada ejercicio: crea una **base de datos** dentro del servidor que ya está corriendo.

## Arranque

Desde la raíz de `Universidad` (no desde `docker/postgres`):

```bash
docker compose up -d
```

Con Podman:

```bash
podman compose up -d
```

Solo un motor:

```bash
docker compose up -d postgres
```

## Credenciales

| Motor | Contenedor | Puerto host | Usuario | Contraseña | Base por defecto |
| --- | --- | --- | --- | --- | --- |
| MySQL 8 | `uni-mysql` | 3306 | `universidad` | `universidad` | `universidad` |
| PostgreSQL 16 | `uni-postgres` | 5432 | `universidad` | `universidad` | `universidad` |

Los scripts en `docker/*/init` solo se ejecutan la **primera** vez que se crea el volumen. Si cambias el init y ya existía el volumen, hay que recrearlo (`docker compose down -v`) o crear la base a mano.

## Cómo usar esto en un ejercicio

1. No copies otro `compose.yml` en la carpeta de la práctica.
2. Crea una base con el nombre del lab, por ejemplo:

```sql
-- PostgreSQL
CREATE DATABASE lab6;

-- MySQL
CREATE DATABASE lab6;
```

3. Conecta la app a `localhost` y al puerto de la tabla de arriba.

Ejemplos de URL:

```text
postgresql+asyncpg://universidad:universidad@127.0.0.1:5432/lab5
mysql+pymysql://universidad:universidad@127.0.0.1:3306/crm_db
```

## Bases ya creadas

**MySQL:** `escuela_db`, `crm_db`, `uni_db`, `empresa_db` (más usuarios `admin` / `dev_user` para prácticas viejas de 8VO).

**PostgreSQL:** `lab4`, `lab5`, `mikedb` (usuario `mike`), `admin_bank` (usuario `user_admin_bank`).

Los `compose.yml` que ya están dentro de entregas antiguas se dejan como evidencia; para trabajo nuevo usa solo este stack.
