# Práctica 3: Análisis Exploratorio de Datos — Titanic

**Materia:** Extracción de conocimientos en Base de Datos  
**Grupo:** 9 IDGS  
**Modalidad:** Individual  
**Metodología:** CRISP-DM (primeros 3 pasos)

**Archivos relacionados:**
- Notebook: `Practica3_EDA_Titanic.ipynb`
- Dataset original: `titanic3.csv`
- Dataset limpio: `titanic_limpio.csv`

---

## Contexto del set de datos

El RMS Titanic era un transatlántico británico operado por la White Star Line. Zarpó el 10 de abril de 1912 desde Southampton con destino a Nueva York (escalas en Cherbourg y Queenstown). La noche del 14 de abril a las 23:40 colisionó contra un iceberg; se hundió a las 02:20 del 15 de abril.

A pesar de tener capacidad para más de 3,300 personas, solo portaba 20 botes salvavidas (capacidad para 1,178). Los botes se arriaron inicialmente a mitad de capacidad por falta de simulacros y confusión en el protocolo de evacuación.

Este dataset es un benchmark clásico en ciencia de datos para analizar cómo factores sociales, demográficos y económicos influyeron en la supervivencia.

### Descripción de variables

| Variable | Descripción |
|---|---|
| `pclass` | Clase del pasajero (1 = 1ª; 2 = 2ª; 3 = 3ª). Aprox. del estatus socioeconómico |
| `survived` | Supervivencia (0 = No; 1 = Sí) |
| `name` | Nombre |
| `sex` | Sexo |
| `age` | Edad |
| `sibsp` | Número de hermanos/cónyuges a bordo |
| `parch` | Número de padres/hijos a bordo |
| `ticket` | Número de boleto |
| `fare` | Tarifa pagada |
| `cabin` | Cabina |
| `embarked` | Puerto de embarque (C = Cherbourg; Q = Queenstown; S = Southampton) |
| `boat` | Bote salvavidas |
| `body` | Número de identificación del cuerpo |
| `home.dest` | Destino / hogar |

---

## Objetivos didácticos

Fortalecer pipelines ETL y EDA guiados por CRISP-DM:

1. **Business Understanding** — objetivos del proyecto
2. **Data Understanding** — estructura, integridad, nulos, duplicados
3. **Data Preparation** — selección, limpieza, imputación, exportación

---

## 1. Business Understanding

**Objetivo:** Identificar qué factores (género, clase social, tamaño de familia, tarifa) influyeron en la probabilidad de supervivencia.

### Preguntas a responder

1. ¿Cómo interactúan el género y la clase social en la probabilidad de supervivencia?
2. ¿Tener una familia pequeña o viajar solo afectó la tasa de supervivencia?
3. ¿Existe una diferencia significativa en la tarifa pagada (*fare*) entre quienes sobrevivieron y quienes no?

---

## ETAPA 1: Extracción y Exploración Inicial

Carga del archivo `titanic3.csv` (lista oficial de pasajeros). Ver notebook: celdas de importación y lectura.

---

## ETAPA 2: Data Understanding

### Paso 1: Estructura, dimensiones y duplicados

- Carga del dataset
- Dimensión (filas, columnas)
- Tipos de datos (`info`, `dtypes`)
- Duplicados: `df.duplicated().sum()`

### Paso 2: Valores nulos y columnas a eliminar

- Conteo de nulos ordenado descendente
- DataFrame con cantidad y porcentaje de nulos

#### a) Estadísticas clave

Resumen con `describe(include="all")`.

#### b) Selección de columnas a eliminar

| Columna | Motivo |
|---|---|
| `body` | ~90% de nulos; solo aplica a fallecidos identificados |
| `cabin` | ~77% de nulos |
| `boat` | Alto % de nulos; leakage (conocer el bote implica supervivencia) |
| `home.dest` | Muchos nulos y poco valor predictivo |
| `ticket` | Identificador; no aporta al análisis de supervivencia |

### Paso 3: Valores únicos

- `nunique()` por columna
- Impresión de valores únicos en columnas con menos de 10 categorías

### Paso 4: Análisis exploratorio

1. Total de pasajeros
2. Conteo y % de sobrevivientes / no sobrevivientes
3. Conteo y % por sexo
4. Sobrevivientes por sexo y % de supervivencia
5. Conteo y % por clase
6. Hombres y mujeres por clase
7. % de supervivencia según `sibsp`
8. % de supervivencia según `parch`

#### Resultados clave del Paso 4

- Tasa global de supervivencia ~**38%**
- Las **mujeres** sobreviven mucho más que los hombres
- La **1ª clase** tiene mejor supervivencia que la 2ª y 3ª
- Viajar con **pocos parientes** (1–2) suele asociarse a mejor supervivencia que ir solo o en familias muy grandes

### Paso 5: Gráficas (Matplotlib)

1. Histograma general de edades
2. Histogramas de edad por supervivencia, separados por sexo
3. Histogramas de edad por clase (sobrevivientes vs no)

#### Hallazgos del EDA gráfico

- Edades concentradas entre **20 y 40 años**
- En **mujeres** predominan las edades asociadas a supervivencia; en **hombres**, la no supervivencia
- En **1ª clase** hay más sobrevivientes relativos; en **3ª** domina la no supervivencia
- Los niños muestran mejor supervivencia relativa

---

## ETAPA 3: Data Preparation

1. Copia del dataframe
2. Columnas relevantes: `pclass`, `survived`, `name`, `sex`, `age`, `sibsp`, `parch`, `fare`, `embarked`
3. Verificación de estructura
4. `sex` numérico: female → 0, male → 1
5. Imputación:
   - `age` → mediana
   - `fare` → mediana
   - `embarked` → moda
6. Verificación de nulos = 0
7. Exportación a `titanic_limpio.csv`

---

## Respuestas a las preguntas de negocio

### 1. ¿Cómo interactúan el género y la clase social?

Las mujeres de 1ª y 2ª clase tienen las tasas más altas. Los hombres de 3ª clase tienen las más bajas. El género es el factor dominante; la clase lo modula (mujer de 3ª sobrevive menos que una de 1ª; hombre de 1ª sobrevive más que uno de 3ª).

### 2. ¿Familia pequeña o viajar solo afectó la supervivencia?

Sí. Viajar en **familia pequeña (2–4)** se asocia a mayor supervivencia que viajar **solo** o en **familia grande (5+)**.

### 3. ¿Hay diferencia significativa en *fare*?

Sí. Quienes sobrevivieron pagaron, en promedio y mediana, **tarifas más altas**, alineado con la clase social y el acceso a botes.

---

## ¿Qué cambios faltan por realizar?

1. Codificar `embarked` (one-hot o labels) para ML
2. Ingeniería de características: `family_size`, `is_alone`, título desde `name`
3. Escalar/normalizar `age` y `fare`
4. Tratar outliers de `fare` (winsorización o log)
5. Eliminar `name` si el objetivo es modelado predictivo
6. Imputar `age` por clase y sexo (en lugar de mediana global)

---

## Conclusiones

- Se aplicó ETL/EDA siguiendo CRISP-DM (Business Understanding, Data Understanding, Data Preparation).
- Se excluyeron columnas con exceso de nulos o irrelevancia (`body`, `cabin`, `boat`, `home.dest`, `ticket`).
- El dataset limpio tiene 9 columnas, `sex` numérico e imputación sin nulos.
- Factores más asociados a supervivencia: **ser mujer**, **1ª/2ª clase**, **familia pequeña** y **tarifas más altas**.

---

## Referencias

- Dataset `titanic3.csv` — lista de pasajeros del RMS Titanic
- Metodología CRISP-DM
- Librerías: Pandas, NumPy, Matplotlib
- Contexto histórico: White Star Line, viaje inaugural abril 1912
