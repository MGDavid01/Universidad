import hashlib
print("=== DEMOSTRACIÓN SIMPLE DE INTEGRIDAD CON HASH ===\n")

# PASO 1: CREAR DOCUMENTO ORIGINAL
documento_original = "Esta fue la Nota Verde"
print("Documento ORIGINAL:")
print(documento_original)

# PASO 2: GENERAR HASH DEL DOCUMENTO ORIGINAL
hash_original = hashlib.sha256(documento_original.encode()).hexdigest()
print("\nHash ORIGINAL generado:")
print(hash_original)

# PASO 3: SIMULAR QUE EL DOCUMENTO ES MODIFICADO
documento_modificado = "Esta fue la Nota Verde."
print("\nDocumento MODIFICADO: ")
print(documento_modificado)

# PASO 4: GENERAR HASH DEL DOCUMENTO MODIFICADO
hash_modificado = hashlib.sha256(documento_modificado.encode()).hexdigest()
print("\nHash del documento MODIFICADO: ")
print(hash_modificado)

# PASO 5: COMPARAR HASHES
print("\nComparando hashes...")
if hash_original == hash_modificado:
    print("Resultado: El documento NO fue alterado.")
else:
    print("Resultado: El documento fue MODIFICADO.")
