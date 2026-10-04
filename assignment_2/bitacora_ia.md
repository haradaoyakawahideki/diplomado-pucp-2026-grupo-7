# Bitácora IA

## Hideki Harada

Utilicé IA (Claude) principalmente para entender las funciones y qué pedía la tarea de mí. Solicité a Claude explícitamente que no realice la tarea por mí, sino que me ayude a entender cómo completar la tarea. La IA fue útil para entender por qué el código fallaba o qué faltaba pese a que el código no botaba alertas. 

## Karen Macedo
Utilicé IA (Claude) como apoyo para entender los pasos del cruce: por qué el ubigeo debe leerse como texto, cómo hacer el merge por ubigeo y cómo armar los gráficos. Revisé los resultados y las respuestas antes de subirlos.

### Entrada – Parte 3
1. Le pedí a la IA un código para verificar los conteos de `decretos_por_departamento.csv` antes del cruce.
2. Me indicó usar `explode()` y luego `pd.crosstab()`.
3. Salió `ValueError: cannot reindex on an axis with duplicate labels`, porque `explode()` repite el índice.
4. Lo corregí agregando `.reset_index(drop=True)` después de `explode()`. Así encontré que el DS 0012-2024-PCM dice "Ancash" sin tilde y no se contó para Áncash; lo anoté como limitación.
