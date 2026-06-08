import hashlib

def generar_hashes(texto):
    hashes = {
        "MD5": hashlib.md5(texto.encode()).hexdigest(),
    }
    return hashes

# Pedir entrada al usuario
palabra = input("Ingresa una palabra:").strip()
resultado = generar_hashes(palabra)

# Mostrar resultados
print("\nHashes generados:")
for algoritmo, hash_valor in resultado.items():
    print(f"{algoritmo}: {hash_valor}")
