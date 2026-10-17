# Práctica 2. Pipeline ETL y limpieza de datos con Pandas

**Alumno:** Mejía González David  
**Materia:** Extracción de conocimientos en Base de Datos  
**Grupo:** 9 IDGS  
**Docente:** M.C. Martha Cárdenas Maciel  
**Fecha:** 12 de octubre de 2026

En esta práctica armé un flujo ETL con Pandas sobre `pokemon.csv`. La idea fue leer el archivo tal como llegó, corregir los problemas de calidad que se notan al inspeccionarlo y dejar un CSV limpio, `pokemon_limpio.csv`, listo para analizarse después.

---

## Fase 1. Extracción

Cargué el archivo con `pd.read_csv()` y, antes de tocar nada, hice una copia de trabajo:

```python
dataFrame_Original = pd.read_csv(archivo_entrada)
dataFrame_Limpio = dataFrame_Original.copy()
```

La copia me sirvió para no perder los datos crudos. Si una corrección salía mal, podía comparar contra el original en lugar de volver a leer el archivo.

El conjunto trae **150 registros y 7 columnas**: `N.º`, `Nombre`, `Tipo1`, `Tipo2`, `Altura`, `Peso` y `Legendario`. En las primeras cinco filas ya se ve el patrón general: número, nombre, uno o dos tipos, altura, peso y un 0 o 1 para indicar si es legendario. Bulbasaur, por ejemplo, queda como Planta/Veneno, 0.7 m y 6.9 kg, no legendario.

Al revisar `info()` noté que las columnas no llegan con el tipo que uno esperaría. `N.º` se lee como texto porque hay valores que no son números puros, como `15 Beedrill` y `14 4`. `Nombre`, `Tipo1` y `Tipo2` también quedan como texto. `Altura` y `Peso` sí entran como numéricos, y `Legendario` entra como flotante (`0.0` y `1.0`) porque tiene huecos.

Las estadísticas del original hay que leerlas con cuidado. La media y los extremos de altura y peso existen, pero varias filas están corridas de columna, así que esos números todavía no describen bien a los Pokémon. En las columnas de texto, `describe()` solo aporta conteos y la categoría más repetida.

Los nulos del archivo original quedaron así:

| Columna | Valores nulos |
|---|---:|
| N.º | 0 |
| Nombre | 0 |
| Tipo1 | 0 |
| Tipo2 | 78 |
| Altura | 0 |
| Peso | 0 |
| Legendario | 6 |

Los 78 nulos de `Tipo2` no son, en su mayoría, un error: muchos Pokémon solo tienen un tipo. Los 6 nulos de `Legendario` sí vienen del desplazamiento de columnas, porque el valor se salió de su lugar y la última celda quedó vacía.

---

## Fase 2. Transformación y limpieza

### Índice de `N.º`

Usé `N.º` como índice para identificar cada registro con su número de Pokédex y no con la posición de la fila. Al final lo regresé como columna con `reset_index()`, porque al exportar con `index=False` no quería perder ese dato en el CSV.

### Espacios en blanco

Varios textos traen espacios al inicio o al final. Se ve en valores como ` Bicho`, ` Normal` o ` Veneno`, y también en nombres como ` Fearow ` o ` Porygon`. Apliqué `str.strip()` a todas las columnas de texto. Sin ese paso, Pandas trataría `Normal` y ` Normal` como categorías distintas, aunque para nosotros sean la misma.

### Registros desplazados

El problema más delicado fue el de las filas corridas. No quise “adivinar” toda la tabla: ubiqué los casos que se ven mal y les reasigné los campos a mano.

En Beedrill, el número y el nombre se guardaron juntos en `N.º` (`15 Beedrill`). Por eso `Tipo1` cayó en `Nombre`, `Tipo2` en `Tipo1`, y al final `Legendario` quedó vacío. Restauré la fila como número 15, Beedrill, Bicho/Veneno, 1.0 m, 29.5 kg y no legendario.

En los monotipo el fallo es otro. Como no se guardó `Tipo2`, la altura se metió en esa columna, el peso se fue a `Altura` y el peso real terminó en 0 o se pasó a `Legendario`. Me pasó con Rattata, Raticate, Dratini, Dragonair y Mewtwo. En esos registros puse `Ninguno` en `Tipo2` y devolví altura, peso y legendario a su columna. Mewtwo sí es legendario, así que ahí dejé 1; los otros quedaron en 0.

Estas correcciones son puntuales. Funcionan porque el archivo es chico y los casos se pueden revisar uno por uno. En un dataset grande no haría esto a ciegas: compararía contra un catálogo de referencia.

### Categorías y errores de escritura

En `Tipo1` y `Tipo2` hay sinónimos, erratas y cambios de mayúsculas. Los unifiqué con `replace()` hacia los nombres de tipo que se usan en el resto del archivo:

| Valor encontrado | Valor unificado |
|---|---|
| Wa ter | Agua |
| Hierba | Planta |
| Insecto | Bicho |
| I ce | Hielo |
| Veneno n | Veneno |
| luchando, Lucha ng | Lucha |
| psíquico | Psíquico |
| hada | Hada |

Además corregí el nombre `Bellspr fuera`, que en realidad es Bellsprout. Ese espacio de más no lo pedía la lista de tipos, pero se nota al leer la fila 69 y deja el nombre partido.

### Valores faltantes

Después de acomodar las filas desplazadas, los nulos que quedan en `Tipo2` sí corresponden a Pokémon de un solo tipo. Los rellené con `fillna("Ninguno")` para que la ausencia quede explícita y no se confunda con un dato perdido.

En `Legendario` usé `fillna(0)`, como pide la práctica. En este archivo esos huecos venían del corrimiento, y al reparar esas filas el valor correcto ya había quedado escrito. El `fillna` se queda como red de seguridad por si quedara algún nulo.

### Tipos de datos

El identificador de Articuno venía como `14 4`. Lo cambié a `144` antes de convertir la columna. Luego pasé `N.º` a entero con `to_numeric` y `astype(int)`, y `Altura` y `Peso` a numérico. `Legendario` lo convertí a booleano, así que `1` queda como `True` y `0` como `False`.

---

## Fase 3. Carga

Exporté el DataFrame limpio con:

```python
dataFrame_Limpio.to_csv(archivo_salida, index=False, encoding="utf-8-sig")
```

`index=False` evita que se agregue una columna extra con el índice de Pandas. Usé `utf-8-sig` para que el archivo abra bien en Excel y no se rompan acentos como el de Psíquico o Eléctrico. El resultado es `pokemon_limpio.csv`, con las mismas 150 filas y 7 columnas, ya sin nulos.

---

## Verificación del resultado

Volví a revisar el DataFrame ya limpio, no el original.

Las primeras 10 filas se ven estables: del 1 al 10, de Bulbasaur a Caterpie, con tipos completos y `Tipo2` en `Ninguno` cuando el Pokémon es monotipo. Charmander, Charmeleon y Squirtle entran en ese caso.

Las últimas 10 filas cubren del 141 al 150. Ahí se comprueba lo que más me importaba corregir: Articuno ya es el 144 y está marcado como legendario, igual que Zapdos, Moltres y Mewtwo. Dratini y Dragonair ya no tienen la altura metida en `Tipo2`; ese campo quedó en `Ninguno`.

En una muestra de 10 registros al azar, con semilla fija para poder repetirla, los tipos ya no traen espacios ni palabras partidas, y `Legendario` solo toma `True` o `False`.

La estructura final es de 150 filas por 7 columnas. `N.º` es entero, `Nombre`, `Tipo1` y `Tipo2` son texto, `Altura` y `Peso` son numéricos, y `Legendario` es booleano.

En las estadísticas ya tiene más sentido leer los números. La altura va de 0.2 m (Diglett) a 8.8 m (Onix), con una media cercana a 1.20 m. El peso va de 0.1 kg (Gastly y Haunter) a 460 kg (Snorlax), con una media cercana a 46.23 kg. Los identificadores van del 1 al 150 y no se repiten. Hay 4 legendarios.

`isnull().sum()` da 0 en todas las columnas. Lo que antes era nulo en `Tipo2` ahora es la categoría `Ninguno`, que es una decisión de limpieza y no un valor perdido.

Los tipos únicos de `Tipo1`, ya sin repetir, son 15:

Agua, Bicho, Dragón, Eléctrico, Fantasma, Fuego, Hada, Hielo, Lucha, Normal, Planta, Psíquico, Roca, Tierra y Veneno.

Desaparecieron las variantes mal escritas (`Wa ter`, `Hierba`, `Insecto`, `luchando`, `Veneno n` y las demás).

Como comprobación extra, revisé que no hubiera identificadores duplicados ni alturas o pesos negativos. No apareció ninguno. También volví a leer el CSV exportado para confirmar que se puede abrir y que conserva las 150 filas y 7 columnas.

---

## ¿Qué cambios faltan y cómo los aplicaría?

El archivo ya se puede usar para un análisis básico, pero no lo daría por cerrado.

Todavía hay nombres partidos que no entré a corregir: `Persia n` (Persian), `G olem` (Golem) y `Kin gler` (Kingler). El mismo criterio que usé con Bellsprout alcanza: localizar el registro y aplicar `replace()` sobre `Nombre`.

Otros nombres están escritos como una traducción libre y no como el nombre con el que aparece el Pokémon en las fuentes en español o en inglés: `Sr. Mimo`, `Electrodo`, `Tauro` y, según el criterio que se elija, `Hipno`. No los cambiaría por intuición. Primero armaría un catálogo de referencia, por ejemplo la Pokédex de la primera generación, y haría un `merge` por `N.º` para ver qué nombres, tipos, alturas y pesos no coinciden. Solo entonces reemplazaría el valor.

También me falta validar altura y peso contra esa misma fuente. Las filas que reparé a mano quedaron coherentes con los ejemplos de la práctica, pero el resto no fue comparado. Un filtro de diferencias, o una regla que marque alturas fuera de un rango razonable, serviría para sacar los casos dudosos sin modificarlos todavía.

Por último, `Ninguno` en `Tipo2` es útil para no dejar nulos, pero en un modelo habría que decidir si esa categoría se conserva o si conviene tratarla otra vez como ausencia. Eso ya depende del análisis, no de la limpieza.

---

## Conclusiones

Con esta práctica me quedó más claro que el ETL no es solo “leer un CSV y guardarlo de nuevo”. La extracción sirvió para ver la forma real del archivo: 150 Pokémon, columnas corridas, espacios de más y tipos escritos de varias maneras. En la transformación tuve que separar lo que es un dato faltante legítimo, como el segundo tipo de un Pokémon monotipo, de lo que es un error de captura, como Beedrill o Articuno. La carga, al final, es la parte corta: exportar `pokemon_limpio.csv` cuando el DataFrame ya aguanta una revisión de nulos, tipos y categorías.

Lo que más me costó fue no corregir de más. En un archivo pequeño es tentador ir arreglando nombres a ojo, pero si no tengo la fuente al lado puedo introducir otro error. Por eso dejé documentadas las correcciones puntuales y, en lo que no pude verificar, preferí señalarlo como pendiente.

---

## Referencias

- Instrucciones de la práctica: *Práctica 2. Pipeline ETL y limpieza de datos con Pandas*.
- Pandas Development Team. *pandas documentation*. https://pandas.pydata.org/docs/
- McKinney, W. (2022). *Python for Data Analysis* (3.ª ed.). O'Reilly Media.
