import hashlib

def generar_hashes(texto):
    return {
        "MD5": hashlib.md5(texto.encode()).hexdigest(),
        "SHA-1": hashlib.sha1(texto.encode()).hexdigest(),
        "SHA-256": hashlib.sha256(texto.encode()).hexdigest(),
    }

# Hashes almacenados (123, Martinez, Angel respectivamente)
hashes_guardados = {
    "MD5": "202cb962ac59075b964b07152d234b70",       # 123
    "SHA-1": "8e342abba263fa4209f9795ce488abf5818428c0",  # Martinez
    "SHA-256": "0160733d2828347f1bad79c3b29e34894f331ee512a606ac5dbe67fd8399978d",  # Angel
}

# Pedir entrada al usuario
palabra = input("Ingresa una palabra: ").strip()
hashes_ingresados = generar_hashes(palabra)

# Comparar hashes
coincidencia = False
for algoritmo, hash_guardado in hashes_guardados.items():
    if hashes_ingresados[algoritmo] == hash_guardado:
        print(f"✅ La palabra ingresada coincide con el hash almacenado ({algoritmo}).")
        coincidencia = True
        break

if not coincidencia:
    print("❌ La palabra ingresada no coincide con ningun hash almacenado.")
