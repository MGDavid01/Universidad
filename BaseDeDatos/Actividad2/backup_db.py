#!/usr/bin/env python3
"""Crea respaldos automáticos de crm_db usando docker exec"""

import subprocess
import os
from datetime import datetime, timedelta

CONTAINER_NAME = "db_crm"
DB_NAME = "crm_db"
DB_USER = "admin"
DB_PASSWORD = "adminpass"
BACKUP_DIR = "./respaldos"
RETENTION_DAYS = 7

os.makedirs(BACKUP_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_file = os.path.join(BACKUP_DIR, f"backup_{DB_NAME}_{timestamp}.sql")

cmd = [
    "docker", "exec", CONTAINER_NAME,
    "mysqldump", f"-u{DB_USER}", f"-p{DB_PASSWORD}",
    "--single-transaction",
    "--routines", "--triggers",
    DB_NAME
]

print(f"Generando respaldo en {backup_file}...")
try:
    with open(backup_file, "w", encoding="utf-8") as f:
        subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE, check=True, text=True)

    size_kb = os.path.getsize(backup_file) / 1024
    print(f"Respaldo creado: {backup_file} ({size_kb:.2f} KB)")
except subprocess.CalledProcessError as e:
    print(f"Error en mysqldump: {e.stderr}")
    exit(1)
except FileNotFoundError:
    print("Docker no encontrado. Asegurate de tener Docker en ejecucion.")
    exit(1)

cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
deleted = 0
for filename in os.listdir(BACKUP_DIR):
    if filename.startswith(f"backup_{DB_NAME}_") and filename.endswith(".sql"):
        path = os.path.join(BACKUP_DIR, filename)
        if datetime.fromtimestamp(os.path.getmtime(path)) < cutoff:
            os.remove(path)
            deleted += 1
            print(f"Eliminado antiguo: {filename}")

print(f"Proceso finalizado. {deleted} archivos antiguos eliminados." if deleted else "Proceso finalizado.")
