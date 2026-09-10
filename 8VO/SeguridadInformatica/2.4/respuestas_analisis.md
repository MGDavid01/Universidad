# Respuestas de Análisis - Práctica 2.4 Comparación de Hashes

## 1. ¿Qué sucede cuando cambias una sola letra?

El hash cambia por completo. Aunque solo modifiques una letra, el resultado es totalmente distinto al original.

---

## 2. ¿Por qué el hash cambia completamente?

Porque el algoritmo está hecho así: cualquier cambio pequeño en el texto hace que el hash salga distinto. Así se nota enseguida si algo se ha alterado.

---

## 3. ¿Es posible saber la palabra original solo viendo el hash?

No. Con el hash no se puede “volver atrás” y recuperar el texto. Solo se puede comprobar si otro texto da el mismo hash.

---

## 4. ¿Por qué este método es útil para contraseñas?

Porque el sistema no guarda la contraseña tal cual, solo su hash. Cuando entras, se calcula el hash de lo que escribes y se compara con el guardado. Si coinciden, es correcto. Así, si alguien ve la base de datos, no ve las contraseñas reales.

---

## 5. ¿El mismo texto siempre genera el mismo hash? ¿Por qué?

Sí. Siempre que pongas el mismo texto, obtienes el mismo hash. Si no fuera así, no podríamos comparar para saber si la contraseña es la correcta.

---

## 6. ¿Qué diferencia observas entre un hash de 3 letras y uno de 20 letras?

En el tamaño del hash, ninguna: siempre sale una cadena de 64 caracteres. Lo que cambia es el contenido: cada texto da un hash distinto, da igual que sea corto o largo.

---

## 7. ¿El tamaño del hash cambia según la longitud del texto original?

No. Da igual que el texto tenga una letra o muchas: el hash siempre tiene el mismo tamaño (64 caracteres en hexadecimal).

---

## 8. ¿El hash distingue entre mayúsculas y minúsculas?

Sí. “seguridad”, “SEGURIDAD” y “Seguridad” dan hashes diferentes, porque para el algoritmo cada letra cuenta tal cual la escribes.
