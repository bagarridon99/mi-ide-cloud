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
