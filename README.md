PROJECT CHARTER: Optimización de Inventario Minorista (Retail)
1. El Problema
Actualmente, 50 tiendas físicas operan de forma aislada generando volúmenes masivos de datos crudos y sucios desde sus sensores y sistemas POS
Esto provoca que los modelos de predicción de demanda sean inexactos y que los costos de almacenamiento en la nube sean muy altos

3. La Solución (Arquitectura Híbrida)
Procesamiento Local (On-Premises): Se limpiarán y normalizarán los datos directamente en cada tienda (eliminando errores y duplicados)

Procesamiento en la Nube (Cloud): Solo se enviarán los indicadores clave agregados a un Data Warehouse centralizado, donde se entrenará un modelo global de Machine Learning

3. Objetivos Clave
Negocio: Reducir los costos de almacenamiento en la nube y lograr pronósticos de demanda más exactos

Técnico: Implementar un procesamiento local eficiente antes de la transmisión de datos

4. Hitos del Proyecto
M01: Reducir en un 40% el volumen de datos mediante la limpieza local en tienda

M02: Consolidar los datos de las 50 tiendas en el Data Warehouse central en la nube

M03: Generar un pronóstico de demanda global con una precisión superior al 85%

5. Tecnologías a Utilizar
El proyecto requerirá el uso de lenguajes como Python y bases de datos SQL, apoyándose en servicios de nube (como AWS o Azure)
Además, se utilizará GitHub para el control de versiones y Docker para asegurar la portabilidad del entorno

---

## Pipeline de Datos — Limpieza y Transformación

### Estructura del Proyecto

```
mi-ide-cloud/
├── data/
│   ├── raw/          # Datasets originales (CSV)
│   └── processed/    # Datasets procesados y transformados
├── procesamiento/
│   └── transformacion.py   # Módulo con las 4 transformaciones
├── orquestador.py    # Script principal del pipeline
└── README.md
```

### Ejecución

```bash
python3 orquestador.py
```

### Datasets

| Dataset | Descripción | Filas |
|---------|-------------|-------|
| TITANIC | Pasajeros del Titanic con datos de supervivencia | 891 |
| Libreria | Catálogo de libros con autor, género y editorial | 15 |
| Clima | Registros diarios de temperatura y humedad por ciudad | 150 |

### Transformaciones Aplicadas (`procesamiento/transformacion.py`)

1. **resumen_supervivencia** — Agrupa los pasajeros del dataset TITANIC según si sobrevivieron o no, generando una tabla de conteo. Resultado almacenado como `TITANIC_supervivencia` en `almacen_datos`.

2. **agregar_unique_key** — Crea la columna `UniqueKey` en el dataset Libreria usando un hash MD5 de 12 caracteres generado a partir de `titulo + autor + año`. Garantiza un identificador único por libro.

3. **promedio_temperatura** — Calcula el promedio de temperatura en grados Celsius agrupado por ciudad a partir del dataset Clima. Resultado almacenado como `Clima_promedio` en `almacen_datos`.

4. **filtrar_menores_titanic** — Elimina del dataset TITANIC todos los registros de pasajeros con edad menor a 10 años. Actualiza la entrada `TITANIC` en `almacen_datos`.
