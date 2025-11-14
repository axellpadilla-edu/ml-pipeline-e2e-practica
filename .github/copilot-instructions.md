# Instrucciones para Agentes de Codificación AI

## Arquitectura General
Este proyecto es un taller práctico de Data Science enfocado en prevenir fugas de información (data leakage) en pipelines de ML. La arquitectura es simple: un script principal en `src/seguridad_pipeline.py` y un notebook interactivo en `notebooks/demo_codigo_seguro.ipynb` que demuestran la regla "Divide antes, transforma después".

- **Componentes principales**: Carga de datos (`data/bike_sharing_demand.csv`), preprocesamiento seguro, y validación de no fuga.
- **Flujo de datos**: Carga → Limpieza → Extracción de features → Split train/test → Escalado (solo en train) → Validación.
- **Decisiones estructurales**: Todo el código está en español para consistencia educativa. Se usa `pathlib` para rutas relativas robustas.

## Flujos de Desarrollo Críticos
- **Instalación de dependencias**: Ejecuta `uv sync` desde la raíz para sincronizar con `pyproject.toml`.
- **Ejecución del pipeline**: Usa `uv run src/seguridad_pipeline.py` para mantener entornos reproducibles.
- **Desarrollo interactivo**: Abre `notebooks/demo_codigo_seguro.ipynb` en VS Code para iterar pasos.
- **Depuración**: Verifica que `StandardScaler` se ajuste solo en `X_train` (línea ~30 en `seguridad_pipeline.py`).

## Convenciones y Patrones Específicos
- **Manejo de fechas**: Extrae `hour` y `is_weekend` de columnas `timestamp` usando `.dt` (ejemplo en `seguridad_pipeline.py` líneas 18-19).
- **Limpieza de datos**: Elimina NA solo en columnas críticas: `['temp', 'humidity', 'windspeed', 'demand']` (línea 22).
- **Split seguro**: Siempre `train_test_split` antes de cualquier transformación (línea 27).
- **Escalado sin fuga**: `scaler.fit_transform(X_train)` seguido de `scaler.transform(X_test)` (líneas 32-33).
- **Documentación**: Comentarios en español explicando cada paso de prevención de fuga.

## Dependencias y Integraciones
- **Herramientas**: `uv` para gestión de dependencias (Python ≥3.14), no uses `pip` directamente.
- **Librerías clave**: `pandas` para manipulación, `scikit-learn` para preprocessing/ML, `numpy` para arrays.
- **Datos**: Dataset local en `data/`; no hay APIs externas ni bases de datos.

## Ejemplos de Patrones
- Para features temporales: `df['hour'] = df['timestamp'].dt.hour` (ver `seguridad_pipeline.py`).
- Para split: `train_test_split(X, y, test_size=0.2, random_state=42)` (línea 27).
- Para escalado seguro: Ajusta solo en train, transforma ambos sets (líneas 32-33).

Mantén la consistencia en español y enfócate en prácticas seguras contra data leakage.