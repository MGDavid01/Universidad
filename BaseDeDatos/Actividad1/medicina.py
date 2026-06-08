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

# 3. Leer los datos y mostrarlos
cursor.execute("SELECT * FROM estudiantes WHERE carrera = 'Medicina'")
for fila in cursor.fetchall():
    print(fila)

# 4. Cerrar todo (buena práctica)
cursor.close()
conn.close()