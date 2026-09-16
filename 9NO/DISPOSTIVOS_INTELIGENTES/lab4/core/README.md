# `core/` — Utilidades transversales

Código compartido que no pertenece a un endpoint concreto: seguridad y configuración de la app.

## Archivos

### `cors.py`
- Función `setup_cors(app, origins=["*"])`.
- Añade el middleware `CORSMiddleware` para permitir peticiones desde otros orígenes (p. ej. un frontend).
- Se llama desde `main.py` al crear la aplicación.

### `security.py`
- Configura `CryptContext` de Passlib con esquema **Argon2**.
- `get_password_hash(password)`: genera el hash de una contraseña.
- `verify_password(plain, hashed)`: comprueba si la contraseña en claro coincide con el hash.

Pensado para usarse al crear/autenticar usuarios (hashear antes de guardar en BD).
