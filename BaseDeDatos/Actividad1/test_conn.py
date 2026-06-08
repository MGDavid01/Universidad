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