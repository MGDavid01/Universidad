import hashlib

def generar_hash(texto):
    """Genera el hash SHA-256 de un texto en formato hexadecimal."""
    texto_bytes = texto.encode()
    hash_obj = hashlib.sha256(texto_bytes)
    return hash_obj.hexdigest()

# Parte 1 - Generación de Hash
print("=== Parte 1: Generación de Hash ===")
palabra = input("Ingresa una palabra: ").strip()
hash_generado = generar_hash(palabra)
print(f"Hash SHA-256: {hash_generado}")

# Parte 2 - Comparación de Hashes
print("\n=== Parte 2: Comparación de Hashes ===")
hash_guardado = generar_hash("seguridad")

palabra_comparar = input("Ingresa una palabra para comparar: ").strip()
hash_ingresado = generar_hash(palabra_comparar)

if hash_ingresado == hash_guardado:
    print("Las palabras coinciden.")
else:
    print("Las palabras NO coinciden.")
