# Assignment 3 – Visualización, mapas y dashboard

## Grupo 7

### Pregunta
**¿Los departamentos con mayor lluvia acumulada son también los que registran más declaratorias de emergencia durante enero–mayo de 2024?**

### Datos
Se reutiliza la **Opción B – Assignment 2 (Emergencias y lluvias)**. El archivo `datos/dataset.csv` corresponde a la tabla final construida por el Grupo 7 en el Assignment 2.

### Hallazgos
1. Los departamentos con mayor lluvia acumulada no coinciden necesariamente con los que registran el máximo número de declaratorias.
2. La relación entre lluvia acumulada y declaratorias es débil, por lo que la lluvia por sí sola no explica el patrón observado.

### Limitaciones
- La lluvia corresponde a la capital departamental.
- El GeoJSON del curso no contiene geometrías para los 25 departamentos; se reportan los no cruces y no se fuerzan coincidencias.
- El análisis es descriptivo; correlación no implica causalidad.

### Dashboard público
**Enlace:** PENDIENTE – reemplazar luego del despliegue en Streamlit Community Cloud.

### Ejecución local
```bash
streamlit run app.py
```
