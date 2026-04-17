# Automatización de limpieza de datos

## ¿Qué hace?
Esté script en python permite limpiar automáticamente archivos CSV con datos sucios (fechas inconsistentes, precios con símbolos, valores nulos).

## ¿Cómo usarlo?
1. Ejecutar: "python limpieza_automatica.py"
2. El script programa limpieza diaria a las 9:00 AM
3. También puede ejecutarse manualmente con "limpiar_datos()"

## Tecnologías
- Python 3.x
- Pandas
- Schedule

## Ejemplo de transformación
| fecha original | fecha limpia |
|----------------|--------------|
| 15/04/2026     | 2026-04-15   |
| $1200          | 1200.00      |
