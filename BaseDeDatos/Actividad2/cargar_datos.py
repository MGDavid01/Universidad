#!/usr/bin/env python3
"""Genera registros de prueba en el CRM (catálogos + oportunidades)."""

import mysql.connector
from faker import Faker

NUM_REGISTROS = 10
DB_CONFIG = {
    "host": "localhost",
    "user": "admin",
    "password": "adminpass",
    "database": "crm_db",
}

ROLES_DISPONIBLES = (1, 2, 3)
ESTADOS_OPORTUNIDAD = ("prospecto", "negociacion", "ganada", "perdida")

fake = Faker("es_ES")

conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

try:
    for _ in range(NUM_REGISTROS):
        cursor.execute(
            "INSERT INTO clientes (nombre, email, telefono, empresa, notas) VALUES (%s, %s, %s, %s, %s)",
            (
                fake.name(),
                fake.unique.email(),
                fake.phone_number(),
                fake.company(),
                fake.sentence(nb_words=6),
            ),
        )
        cliente_id = cursor.lastrowid

        precio = round(fake.pyfloat(min_value=10, max_value=5000, right_digits=2), 2)
        cursor.execute(
            "INSERT INTO productos (nombre, descripcion, precio, stock, activo) VALUES (%s, %s, %s, %s, %s)",
            (
                fake.catch_phrase()[:100],
                fake.text(max_nb_chars=120),
                precio,
                fake.random_int(min=0, max=200),
                True,
            ),
        )
        producto_id = cursor.lastrowid

        cursor.execute(
            "INSERT INTO usuarios (nombre, email, password, role_id, activo) VALUES (%s, %s, %s, %s, %s)",
            (
                fake.name(),
                fake.unique.email(),
                fake.password(length=12),
                fake.random_element(ROLES_DISPONIBLES),
                fake.boolean(chance_of_getting_true=90),
            ),
        )
        usuario_id = cursor.lastrowid

        cursor.execute(
            """INSERT INTO oportunidades
               (cliente_id, producto_id, usuario_id, titulo, estado, valor_estimado,
                fecha_cierre_esperada, notas)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                cliente_id,
                producto_id,
                usuario_id,
                fake.sentence(nb_words=4)[:150],
                fake.random_element(ESTADOS_OPORTUNIDAD),
                round(precio * fake.random_int(min=1, max=5), 2),
                fake.date_between(start_date="today", end_date="+90d"),
                fake.paragraph(nb_sentences=2),
            ),
        )

    conn.commit()
    print(
        f"Se cargaron {NUM_REGISTROS} registros por tabla: "
        "clientes, productos, usuarios y oportunidades."
    )
    print("Los roles iniciales vienen del seed en init.sql.")
except Exception as e:
    print(f"Error al insertar: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
