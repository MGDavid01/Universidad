# Actividad: Primeros pasos con MySQL en Docker

> **Duración estimada:** 45–60 minutos  
> **Materia:** Base de Datos

---

## 🎯 Objetivos de la clase

Al finalizar esta actividad podrás:

1. Levantar un contenedor MySQL usando Docker.
2. Conectarte a MySQL desde **MySQL Workbench** y desde **Python**.
3. Crear una tabla, insertar datos y ejecutar consultas `SELECT`.
4. Explicar con tus propias palabras qué es un contenedor, un volumen y un puerto en Docker.

---

## 📖 Conceptos clave (leé esto primero)

Antes de ejecutar comandos, entendamos qué estamos haciendo:

| Concepto | ¿Qué es? | Analogía |
|----------|----------|----------|
| **Docker** | Programa que ejecuta "contenedores" | Como una máquina virtual liviana |
| **Contenedor** | Entorno aislado con todo lo necesario para que un programa funcione | Una caja sellada que contiene MySQL y todo lo que necesita |
| **Imagen** | Plantilla para crear contenedores | El molde con el que se hornea un pastel |
| **Puerto `-p`** | "Puerta" por la que tu PC y el contenedor se comunican | Un teléfono: el 3306 es el número de MySQL |
| **Volumen `-v`** | Carpeta especial que guarda datos aunque borres el contenedor | Una caja de seguridad fuera de la caja |
| **Variable `-e`** | Configuración que le pasamos al contenedor al crearlo | Instrucciones escritas en la tapa de la caja |

> 💡 **Pregunta para pensar:** ¿Qué crees que pasa con los datos de la BD si detenemos el contenedor? ¿Y si lo eliminamos? (Lo responderemos al final).

---

## 🔹 Paso 1: Crear y ejecutar el contenedor MySQL

Vamos a pedirle a Docker que cree un contenedor con MySQL 8.

> ⚠️ **Importante para Windows CMD:** Copia y pega el comando **exactamente en una sola línea**. No agregues saltos de línea.

```cmd
docker run --name mysql-clase -e MYSQL_ROOT_PASSWORD=clase123 -e MYSQL_DATABASE=escuela_db -p 3306:3306 -v mysql_datos:/var/lib/mysql -d mysql:8
```

### 📌 ¿Qué acaba de pasar? (Explicación línea por línea)

| Parte | Significa |
|-------|-----------|
| `docker run` | "Docker, creá y ejecutá un contenedor" |
| `--name mysql-clase` | Le ponemos nombre al contenedor |
| `-e MYSQL_ROOT_PASSWORD=clase123` | Le decimos "la contraseña de root es `clase123`" |
| `-e MYSQL_DATABASE=escuela_db` | Le decimos "creá automáticamente una BD llamada `escuela_db`" |
| `-p 3306:3306` | "Abrí la puerta 3306 para que podamos conectarnos" (el de la derecha es puerto interno de MySQL, el de la izquierda es el puerto en tu PC) |
| `-v mysql_datos:/var/lib/mysql` | "Guardá los datos en un volumen persistente" |
| `-d` | "Ejecutalo en segundo plano" (modo demonio) |
| `mysql:8` | "Usá la imagen oficial de MySQL versión 8" |

### 🧪 Verificá tu comprensión

Tápá la tabla de arriba y respondsé:

1. ¿Qué cambia si escribo `-p 3307:3306` en lugar de `-p 3306:3306`?
2. ¿Qué pasaría si omito `-v mysql_datos:/var/lib/mysql`?
3. ¿Para qué sirve el `-d` al final?

---

## 🔹 Paso 2: Verificar que el contenedor está corriendo

```cmd
docker ps
```

✅ Debes ver algo como:

```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS                    NAMES
abc123...      mysql:8   "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:3306->3306/tcp   mysql-clase
```

> ⏱️ **Importante:** La primera vez MySQL tarda **10–15 segundos** en inicializarse. Si ves `STATUS` = `Up` ya está listo. Si ves `STATUS` = `starting` esperá unos segundos más.

Para ver los logs en vivo (útil para saber si ya terminó de arrancar):

```cmd
docker logs -f mysql-clase
```

Verás algo como `[Server] /usr/sbin/mysqld: ready for connections.` → ¡ya está listo!

Presioná `Ctrl + C` para salir de la vista de logs.

### 🧪 Verificá tu comprensión

4. ¿Qué comando usarías para saber si el contenedor está corriendo?
5. ¿Cómo diferenciás en `docker ps` si un contenedor está listo o todavía iniciando?

---

## 🔹 Paso 3: Conectarte a la Base de Datos

Elegí **UNA** de las siguientes dos opciones.

---

### 🟦 Opción A: MySQL Workbench (Entorno gráfico)

1. Abrí MySQL Workbench.
2. Hacé clic en el botón `+` que está al lado de *MySQL Connections*.
3. Configurá estos datos exactamente:

| Campo | Valor |
|-------|-------|
| Connection Name | `Clase MySQL` |
| Connection Method | `Standard (TCP/IP)` |
| Hostname | `127.0.0.1` |
| Port | `3306` |
| Username | `root` |
| Password | `clase123` (clic en *Store in Keychain* si lo pide) |

4. Clic en **Test Connection** → debe aparecer `Successfully made the connection`.
5. Clic en **OK** → clic en la conexión nueva para abrirla.

> ⚠️ **Error común:** Si te sale `Can't connect to MySQL server on '127.0.0.1'`, revisá que:
> - Docker Desktop esté abierto
> - El contenedor esté corriendo (`docker ps`)
> - Esperaste 15 segundos después de crearlo

---

### 🟨 Opción B: Python (Editor de código / Terminal)

1. Instalá el driver oficial de MySQL para Python:

```bash
pip install mysql-connector-python
```

2. Creá un archivo llamado `test_conn.py` con este contenido:

```python
import mysql.connector

try:
    # Intentamos conectarnos al servidor MySQL que corre en Docker
    conn = mysql.connector.connect(
        host="127.0.0.1",    # es lo mismo que "localhost"
        user="root",          # usuario administrador (solo para prácticas)
        password="clase123",  # la contraseña que pusimos en el docker run
        database="escuela_db" # la BD que se creó automáticamente
    )
    print("✅ Conexión exitosa a MySQL")
    conn.close()  # siempre cerrar la conexión
except Exception as e:
    print("❌ Error de conexión:", e)
```

3. Ejecutá el archivo:

```bash
python test_conn.py
```

Si ves el mensaje verde, ¡todo funciona! Si ves un error, revisá el checklist del error común de arriba.

---

## 🔹 Paso 4: Crear tablas e insertar datos

Ahora vamos a crear nuestra primera tabla y a guardar datos en ella.

> 💡 **Importante:** Ejecutá estos comandos **solo una vez**. Si ya existe la tabla, podemos usar `IF NOT EXISTS` para evitar errores.

---

### 📝 Con MySQL Workbench

Abrí una nueva pestaña SQL (`File → New Query Tab` o `Ctrl + T`) y ejecutá:

```sql
-- Crear la tabla 'estudiantes'
-- IF NOT EXISTS evita error si la tabla ya existe
CREATE TABLE IF NOT EXISTS estudiantes (
    id INT AUTO_INCREMENT PRIMARY KEY,   -- id único que se genera solo
    nombre VARCHAR(100) NOT NULL,         -- texto de hasta 100 caracteres, obligatorio
    edad INT CHECK (edad > 0),            -- número entero, debe ser positivo
    carrera VARCHAR(100)                  -- texto de hasta 100 caracteres (opcional)
);

-- Insertar 3 estudiantes de ejemplo
INSERT INTO estudiantes (nombre, edad, carrera) VALUES
    ('Ana López', 20, 'Ingeniería de Sistemas'),
    ('Carlos Ruiz', 22, 'Medicina'),
    ('María Torres', 19, 'Diseño Gráfico');

-- Ver los datos que acabamos de insertar
SELECT * FROM estudiantes;
```

**Explicación del CREATE TABLE:**

| Parte | Significa |
|-------|-----------|
| `id INT` | Columna llamada `id`, tipo número entero |
| `AUTO_INCREMENT` | Cada nuevo estudiante recibe automáticamente el siguiente número (1, 2, 3...) |
| `PRIMARY KEY` | Esta columna es el identificador único de cada fila |
| `VARCHAR(100)` | Texto de hasta 100 caracteres |
| `NOT NULL` | Esta columna no puede estar vacía |
| `CHECK (edad > 0)` | Regla: la edad debe ser mayor a 0 |
| `INSERT INTO ... VALUES` | Agrega filas a la tabla |
| `SELECT * FROM ...` | Trae todas las columnas (`*`) de la tabla |

Seleccioná todo el código y presioná `⚡` (Execute) o `Ctrl + Enter`.

---

### 🐍 Con Python

Creá un archivo `crear_datos.py`:

```python
import mysql.connector

# 1. Conectar a la base de datos
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="clase123",
    database="escuela_db"
)

# 2. Crear un cursor: es como un "puntero" para ejecutar comandos
cursor = conn.cursor()

# 3. Crear la tabla (si no existe)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL,
        edad INT,
        carrera VARCHAR(100)
    )
""")
print("✅ Tabla 'estudiantes' lista")

# 4. Insertar datos usando parámetros (%s) en lugar de valores fijos
#    Esto es más seguro y evita errores de tipos
datos = [
    ("Ana López", 20, "Ingeniería de Sistemas"),
    ("Carlos Ruiz", 22, "Medicina"),
    ("María Torres", 19, "Diseño Gráfico")
]

cursor.executemany(
    "INSERT INTO estudiantes (nombre, edad, carrera) VALUES (%s, %s, %s)",
    datos
)

conn.commit()  # ⚠️ OBLIGATORIO: guarda los cambios en la BD
print(f"✅ {cursor.rowcount} filas insertadas.")

# 5. Leer los datos y mostrarlos
cursor.execute("SELECT * FROM estudiantes")
for fila in cursor.fetchall():
    print(fila)

# 6. Cerrar todo (buena práctica)
cursor.close()
conn.close()
```

Ejecutá:

```bash
python crear_datos.py
```

**Explicación del código:**

| Parte | Significa |
|-------|-----------|
| `conn = mysql.connector.connect(...)` | Abre una conexión con la base de datos |
| `cursor = conn.cursor()` | Crea un cursor para ejecutar comandos SQL |
| `cursor.execute("CREATE TABLE...")` | Ejecuta un comando SQL |
| `cursor.executemany(...)` | Ejecuta el mismo INSERT muchas veces con distintos datos |
| `%s` | Marcador de posición (placeholder) que se reemplaza con valores reales |
| `conn.commit()` | Guarda los cambios en la BD (sin esto no se persiste nada) |
| `cursor.fetchall()` | Obtiene todas las filas del resultado del SELECT |
| `cursor.close()` / `conn.close()` | Libera recursos |

---

## 🔹 Paso 5: Gestión rápida del contenedor

Comandos útiles para el día a día:

| Acción | Comando (CMD/Terminal) |
|--------|------------------------|
| Detener el contenedor | `docker stop mysql-clase` |
| Iniciarlo de nuevo | `docker start mysql-clase` |
| Ver logs en vivo | `docker logs -f mysql-clase` |
| Eliminar contenedor | `docker rm -f mysql-clase` |
| Eliminar contenedor + datos | `docker rm -f mysql-clase && docker volume rm mysql_datos` |

> ⚠️ Si eliminás el contenedor con `docker rm -f` sin borrar el volumen, al crear uno nuevo con `-v mysql_datos` recuperarás los datos viejos.

---

## 🛠️ Solución de problemas comunes

| Síntoma | Causa probable | Solución |
|---------|----------------|----------|
| `Error 2003: Can't connect` | MySQL aún no terminó de iniciar | Esperá 10-15s. Verificá con `docker logs mysql-clase` |
| Puerto 3306 ocupado | Otro servicio (o MySQL local) usa el puerto | Cambiá `-p 3307:3306` en `docker run` y conectate a `127.0.0.1:3307` |
| `Authentication plugin 'caching_sha2_password'` | Driver/Workbench muy antiguo | Recreá el contenedor añadiendo `--default-auth=mysql_native_password` |
| Python ejecuta pero no guarda datos | Falta `conn.commit()` | Agregá `conn.commit()` después de `INSERT`/`CREATE` |
| `Table doesn't exist` | Ejecutaste SELECT antes de CREATE | Verificá el orden o usá `IF NOT EXISTS` |

---

## ➕ Mini-ejercicios (para practicar)

Elegí al menos **dos** de los siguientes ejercicios:

### Ejercicio 1: Agregar más estudiantes
Insertá **3 estudiantes nuevos** a la tabla `estudiantes` con tus propios nombres, edades y carreras. Luego mostrá toda la tabla con `SELECT *`.

### Ejercicio 2: SELECT con filtro (WHERE)
Escribí una consulta que muestre solo los estudiantes de una carrera específica (ej: `WHERE carrera = 'Medicina'`).

### Ejercicio 3: Crear una nueva tabla
Creá una tabla llamada `profesores` con las columnas:
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `nombre` (VARCHAR(100), NOT NULL)
- `materia` (VARCHAR(100))
- `email` (VARCHAR(100))

Insertá 2 profesores y mostrá el resultado.

### Ejercicio 4: Actualizar y eliminar
```sql
-- Actualizar un registro
UPDATE estudiantes SET edad = 21 WHERE nombre = 'Ana López';

-- Eliminar un registro
DELETE FROM estudiantes WHERE nombre = 'Carlos Ruiz';

-- Ver el resultado
SELECT * FROM estudiantes;
```

> 💡 ¿Qué pasa si corres `DELETE` sin `WHERE`? (¡Respuesta: se borra toda la tabla!)

---

## 📝 Para entregar

Al finalizar la clase, creá un archivo `entregable_clase.pdf` que contenga:

1. capturas de pantalla
2. El código SQL de los ejercicio 
3. Una respuesta breve a esta pregunta: **"¿Qué diferencia hay entre `docker stop` y `docker rm`?"**
4. conclusion 

---

## 🧠 Preguntas de cierre (discusión en clase)

1. ¿Por qué usamos `-p 3306:3306` y no simplemente `3306`?
2. ¿Qué pasa con los datos si ejecuto `docker rm -f mysql-clase` sin borrar el volumen?
3. ¿Por qué es importante usar `conn.commit()` en Python pero en Workbench los cambios se guardan automáticamente?
4. ¿Cuál es la diferencia entre `docker ps` y `docker ps -a`? (Probalo si no sabés)

---

## 💡 Tips para la clase

1. **Persistencia garantizada:** El volumen `-v mysql_datos:/var/lib/mysql` evita que se pierdan las tablas al reiniciar Docker.
2. **Seguridad básica:** En producción nunca uses `root`. Creá usuarios con `CREATE USER` y asigná permisos con `GRANT`.
3. **Buenas prácticas SQL:** Usá `IF NOT EXISTS`, validá con `CHECK` y siempre parametrizá consultas en Python (`%s` en lugar de cadenas formateadas).
4. **Backup rápido:**
   ```cmd
   docker exec mysql-clase mysqldump -u root -pclase123 escuela_db > backup.sql
   ```
5. **Restaurar backup:**
   ```cmd
   docker exec -i mysql-clase mysql -u root -pclase123 escuela_db < backup.sql
   ```
