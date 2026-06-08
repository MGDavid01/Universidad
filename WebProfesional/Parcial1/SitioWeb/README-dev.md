# Desarrollo Uni (Distrobox `dev` + Podman)

Todo el stack de desarrollo corre **dentro de Distrobox `dev`** y **Podman** (sin instalar PHP/MySQL en Bazzite con rpm).

## Estructura

| Ruta | Uso |
|------|-----|
| `8vo/WebProfesional/Parcial1/SitioWeb/tecnixvw/` | WordPress (sitio actual) |
| `8vo/WebProfesional/Parcial1/SitioWeb/tecnixview/` | Copia de datos MariaDB (`.frm` / `.ibd`) — respaldo para restaurar |

## Servicios (Pod `dev-stack`)

- **MariaDB 10.4** en contenedor `mariadb` (compatible con tus archivos `tecnixview`)
- Puerto **3306** → `127.0.0.1:3306`
- PHP sirve WordPress en **8888** (el pod reserva 8080 para uso futuro, p. ej. otro contenedor)

Credenciales: usuario `root`, contraseña `root`, base de datos `tecnixview`.

## Comandos (desde `distrobox enter dev`)

```bash
dev-stack-up          # Arranca MariaDB
dev-wp-serve          # Sirve tecnixvw en http://127.0.0.1:8888
dev-stack-down        # Para el pod
dev-wp-db-restore     # Vuelve a importar datos desde SitioWeb/tecnixview/
```

Ruta base del parcial:

`/home/Exodus/Documents/Uni/8vo/WebProfesional/Parcial1/SitioWeb/`

## Referencias oficiales

- [Distrobox](https://distrobox.it/) — entorno mutable en Bazzite
- [Bazzite – Distrobox](https://docs.bazzite.gg/Installing_and_Managing_Software/Distrobox/)
- [Podman pods](https://docs.podman.io/en/latest/markdown/podman-pod-create.1.html)
- [MariaDB – IMPORT TABLESPACE](https://mariadb.com/kb/en/innodb-file-per-table-tablespaces/)

## Notas

- El contenedor `mysql` (MySQL 9.7) **no** lee tus `.frm` de MariaDB 10.4; se usa **MariaDB 10.4** en el pod.
- `wp-config.php` ya apunta a `127.0.0.1:3306` y URLs locales `http://127.0.0.1:8888`.
