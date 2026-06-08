# Actividad 2 — CRM básico en Docker

**Tema:** CRM (Customer Relationship Management) minimalista: **clientes**, **productos**, **usuarios**, **roles** y **oportunidades** de venta que enlazan las tres entidades de negocio.

**Stack:** MySQL 8.0 en Docker, Python (`mysql-connector-python`, `Faker`), respaldo con `mysqldump`.

---

## Índice

1. [Modelo de datos — 5 tablas](#1-modelo-de-datos--5-tablas)
2. [Comandos ejecutados y capturas](#2-comandos-ejecutados-y-capturas)
3. [Script de respaldo (`backup_db.py`)](#3-script-de-respaldo-backup_dbpy)
4. [Errores encontrados y soluciones](#4-errores-encontrados-y-soluciones)
5. [Prueba de restauración](#5-prueba-de-restauración)

---

## 1. Modelo de datos — 5 tablas

Cuatro tablas de catálogo y seguridad, más **`oportunidades`** como núcleo comercial: une un cliente, un producto de interés y el vendedor responsable.

### Propósito del CRM

| Área | Tabla | Uso en el negocio |
|------|-------|-------------------|
| Cartera | `clientes` | Personas o empresas con las que se mantiene relación comercial. |
| Catálogo | `productos` | Oferta (servicios o artículos) con precio e inventario. |
| Acceso | `usuarios` | Empleados que usan el CRM (login, perfil). |
| Seguridad | `roles` | Perfiles de permiso (Administrador, Vendedor, Soporte). |
| Pipeline | `oportunidades` | Posible venta: quién compra, qué producto y qué vendedor la gestiona. |

### 1.1 `roles`

| Campo | Tipo | Restricción | Motivo |
|-------|------|-------------|--------|
| `id` | INT | PK, AUTO_INCREMENT | Identificador del rol. |
| `nombre` | VARCHAR(50) | NOT NULL, UNIQUE | Nombre corto y sin duplicados (Admin, Vendedor…). |
| `descripcion` | VARCHAR(255) | opcional | Texto legible del alcance del rol. |

Se crea **primera** porque `usuarios` depende de ella. El `init.sql` inserta tres roles base con `INSERT IGNORE`.

### 1.2 `usuarios`

| Campo | Tipo | Restricción | Motivo |
|-------|------|-------------|--------|
| `id` | INT | PK | Identidad interna. |
| `nombre` | VARCHAR(100) | NOT NULL | Nombre en pantalla y reportes. |
| `email` | VARCHAR(100) | UNIQUE, NOT NULL | Usuario de acceso único. |
| `password` | VARCHAR(255) | NOT NULL | Credencial (en producción: hash bcrypt/argon2). |
| `role_id` | INT | FK → `roles`, RESTRICT | Cada usuario tiene **un** rol asignado. |
| `activo` | BOOLEAN | DEFAULT TRUE | Desactivar sin borrar historial. |

**Relación:** muchos usuarios → un rol (`usuarios.role_id` → `roles.id`). `ON DELETE RESTRICT` evita borrar un rol que aún tiene usuarios asignados.

### 1.3 `clientes`

| Campo | Tipo | Restricción | Motivo |
|-------|------|-------------|--------|
| `id` | INT | PK | Clave del contacto. |
| `nombre` | VARCHAR(100) | NOT NULL | Persona de contacto o nombre comercial. |
| `email` | VARCHAR(100) | UNIQUE, NOT NULL | Canal principal y deduplicación. |
| `telefono` | VARCHAR(20) | opcional | Teléfono de seguimiento. |
| `empresa` | VARCHAR(100) | opcional | Organización asociada (típico en CRM B2B). |
| `notas` | TEXT | opcional | Observaciones del vendedor o soporte. |

Sin FK salientes; las oportunidades referencian a cada cliente.

### 1.4 `productos`

| Campo | Tipo | Restricción | Motivo |
|-------|------|-------------|--------|
| `id` | INT | PK | Referencia del ítem en catálogo. |
| `nombre` | VARCHAR(100) | NOT NULL | Nombre comercial. |
| `descripcion` | VARCHAR(255) | opcional | Detalle breve del producto o servicio. |
| `precio` | DECIMAL(10,2) | NOT NULL | Precio con dos decimales. |
| `stock` | INT | NOT NULL, DEFAULT 0 | Unidades disponibles. |
| `activo` | BOOLEAN | DEFAULT TRUE | Ocultar del catálogo sin eliminar fila. |

Catálogo referenciado por oportunidades; no se elimina un producto si tiene oportunidades abiertas (`ON DELETE RESTRICT`).

### 1.5 `oportunidades`

| Campo | Tipo | Restricción | Motivo |
|-------|------|-------------|--------|
| `id` | INT | PK | Identificador del deal. |
| `cliente_id` | INT | FK → `clientes`, CASCADE | Cliente potencial. |
| `producto_id` | INT | FK → `productos`, RESTRICT | Producto o servicio ofertado. |
| `usuario_id` | INT | FK → `usuarios`, RESTRICT | Vendedor asignado. |
| `titulo` | VARCHAR(150) | NOT NULL | Nombre corto del trato (ej. “Licencias 2026 – Acme”). |
| `estado` | ENUM | prospecto / negociacion / ganada / perdida | Etapas del embudo de ventas. |
| `valor_estimado` | DECIMAL(12,2) | NOT NULL | Monto esperado (puede superar precio unitario × cantidad). |
| `fecha_cierre_esperada` | DATE | opcional | Fecha objetivo de cierre. |
| `notas` | TEXT | opcional | Seguimiento del vendedor. |
| `creado_en` | DATETIME | DEFAULT now | Auditoría de alta. |

**Relaciones:** cada oportunidad conecta exactamente un cliente, un producto y un usuario (vendedor). Es la tabla que da sentido comercial al CRM sin llegar a facturación.

### Resumen de relaciones

```
roles (1) ──< usuarios (1) ──< oportunidades >── (1) clientes
                              oportunidades >── (1) productos
```

- Usuario → rol (N:1).
- Oportunidad → cliente, producto, usuario (N:1 en cada caso).
- Borrar cliente elimina sus oportunidades (`CASCADE`).
- Borrar producto o vendedor con oportunidades activas **falla** (`RESTRICT`) para no perder historial por error.

---

## 2. Comandos ejecutados y capturas

> Guarda cada captura en `capturas/` con el nombre indicado.

### Paso 0 — Requisitos

```powershell
cd "C:\Users\hp user\Documents\UNI\BASE DE DATOS\Activdad 2"
pip install mysql-connector-python faker
```

![Requisitos](./capturas/00-requisitos.png)

---

### Paso 1 — Levantar MySQL

Si ya tenías un volumen con el esquema anterior (viajes/ventas), recrea el volumen:

```powershell
docker compose down -v
docker compose up -d
docker compose ps
docker logs db_crm --tail 30
```

**Verificar:** contenedor `db_crm` en estado `healthy`.

![Docker Compose](./capturas/01-docker-compose-up.png)

---

### Paso 2 — Comprobar tablas y roles iniciales

```powershell
docker exec -it db_crm mysql -u admin -padminpass -e "USE crm_db; SHOW TABLES;"
docker exec -it db_crm mysql -u admin -padminpass -e "SELECT * FROM crm_db.roles;"
```

**Esperado:** cinco tablas y 3 filas en `roles`.

![Tablas del CRM](./capturas/02-show-tables.png)

---

### Paso 3 — Cargar datos de prueba

```powershell
python cargar_datos.py
```

```powershell
docker exec -it db_crm mysql -u admin -padminpass crm_db -e "
  SELECT COUNT(*) AS clientes FROM clientes;
  SELECT COUNT(*) AS productos FROM productos;
  SELECT COUNT(*) AS usuarios FROM usuarios;
  SELECT COUNT(*) AS oportunidades FROM oportunidades;
"
docker exec -it db_crm mysql -u admin -padminpass crm_db -e "
  SELECT o.id, o.titulo, o.estado, c.nombre AS cliente, p.nombre AS producto, u.nombre AS vendedor
  FROM oportunidades o
  JOIN clientes c ON c.id = o.cliente_id
  JOIN productos p ON p.id = o.producto_id
  JOIN usuarios u ON u.id = o.usuario_id
  LIMIT 5;
"
```

![Carga de datos](./capturas/03-cargar-datos.png)

---

### Paso 4 — Respaldo

```powershell
python backup_db.py
dir .\respaldos\
```

![Respaldo](./capturas/05-backup-generado.png)

---

### Paso 5 — Restauración

Ver [sección 5](#5-prueba-de-restauración).

![Restauración](./capturas/06-restauracion.png)

---

## 3. Script de respaldo (`backup_db.py`)

### Conexión

1. Ejecuta `docker exec db_crm mysqldump ...` desde el host.
2. Usuario `admin`, base `crm_db`, salida en `./respaldos/backup_crm_db_<timestamp>.sql`.

### Flags

| Flag | Función |
|------|---------|
| `--single-transaction` | Volcado consistente en InnoDB sin bloqueos largos. |
| `--routines` | Incluye procedimientos almacenados. |
| `--triggers` | Incluye triggers. |

### Limpieza

`RETENTION_DAYS = 7`: elimina archivos `backup_crm_db_*.sql` cuya fecha de modificación sea anterior a hace 7 días.

---

## 4. Errores encontrados y soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| Tablas viejas (`ventas`, etc.) | Volumen Docker persistía esquema anterior | `docker compose down -v` y `up -d` de nuevo. |
| `init.sql` no se reaplica | MySQL solo ejecuta scripts en el primer arranque del volumen | Borrar volumen o usar contenedor nuevo. |
| `Duplicate entry` en emails | Faker repite correos en muchas iteraciones | `fake.unique.email()` en `cargar_datos.py`. |
| No se puede borrar un rol | Usuarios con `role_id` y `ON DELETE RESTRICT` | Reasignar usuarios o borrar usuarios de prueba antes de eliminar el rol. |
| Contenedor no encontrado | Nombre antiguo `db_gestion_viajes` | Usar `db_crm` (actualizado en Compose y scripts). |

---

## 5. Prueba de restauración

Tabla recomendada: **`oportunidades`** (tabla transaccional pequeña; solo tiene FK salientes, no otras tablas dependen de ella).

### 5.1 Respaldo y estado inicial

```powershell
python backup_db.py
docker exec -it db_crm mysql -u admin -padminpass crm_db -e "SELECT COUNT(*) AS total FROM oportunidades;"
```

### 5.2 Simular pérdida

```powershell
docker exec -it db_crm mysql -u admin -padminpass crm_db -e "DROP TABLE oportunidades;"
docker exec -it db_crm mysql -u admin -padminpass crm_db -e "SHOW TABLES;"
```

### 5.3 Restaurar

```powershell
$BACKUP = ".\respaldos\backup_crm_db_YYYYMMDD_HHMMSS.sql"
Get-Content $BACKUP | docker exec -i db_crm mysql -u admin -padminpass crm_db
```

### 5.4 Verificar

```powershell
docker exec -it db_crm mysql -u admin -padminpass crm_db -e "SELECT COUNT(*) AS total FROM oportunidades; DESCRIBE oportunidades;"
```

| Momento | Acción | Resultado |
|---------|--------|-----------|
| T0 | `python backup_db.py` | Archivo en `respaldos/` |
| T1 | `COUNT(*)` en `oportunidades` | N filas |
| T2 | `DROP TABLE oportunidades` | Tabla eliminada |
| T3 | Restaurar `.sql` | Sin error fatal |
| T4 | `COUNT(*)` en `oportunidades` | Mismo total que T1 |

---

## Estructura del proyecto

```
Activdad 2/
├── docker-compose.yml
├── init.sql
├── cargar_datos.py
├── backup_db.py
├── respaldos/
├── capturas/
└── README.md
```

## Referencias rápidas

| Elemento | Valor |
|----------|--------|
| Contenedor | `db_crm` |
| Base de datos | `crm_db` |
| Usuario / contraseña | `admin` / `adminpass` |
| Puerto | `3306` |
| Tablas | `roles`, `usuarios`, `clientes`, `productos`, `oportunidades` |

---

*CRM básico: cinco tablas, embudo de oportunidades, respaldo y restauración documentados sin diagrama ER.*
