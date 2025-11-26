# Instrucciones para Agentes de Codificación AI

## Arquitectura General
Este proyecto es un taller práctico de Data Science enfocado en prevenir fugas de información (data leakage) en pipelines de ML. La arquitectura incluye scripts principales en `src/`, un módulo reutilizable en `src/ml_pipeline_e2e_practica/`, y notebooks interactivos en `notebooks/` que demuestran la regla "Divide antes, transforma después".

- **Componentes principales**: Carga de datos (`data/bike_sharing_demand.csv`), preprocesamiento seguro (`preprocesamiento_seguro.py`), entrenamiento de modelos (`train_regression.py`, `train_classification.py`), y validación de no fuga.
- **Flujo de datos**: Carga → Limpieza → Extracción de features → Split train/test → Escalado (solo en train) → Entrenamiento y evaluación.
- **Decisiones estructurales**: Todo el código está en español para consistencia educativa. Se usa `pathlib` para rutas relativas robustas. El módulo `ml_pipeline_e2e_practica` contiene funciones compartidas para evitar duplicación.

## Flujos de Desarrollo Críticos
- **Instalación de dependencias**: Ejecuta `uv sync` desde la raíz para sincronizar con `pyproject.toml`.
- **Ejecución del pipeline**: Usa `uv run src/seguridad_pipeline.py` para el pipeline básico, o `uv run src/train_regression.py` / `uv run src/train_classification.py` para experimentos de modelos.
- **Desarrollo interactivo**: Abre `notebooks/demo_codigo_seguro.ipynb` en VS Code para iterar pasos del pipeline, o `notebooks/demo_comparativa_modelos.ipynb` para comparar modelos con/sin fuga.
- **Depuración**: Verifica que `StandardScaler` se ajuste solo en `X_train` (líneas 32-33 en `seguridad_pipeline.py` o en `preprocesamiento_seguro.py`).

## Convenciones y Patrones Específicos
- **Manejo de fechas**: Extrae `hour` y `is_weekend` de columnas `timestamp` usando `.dt` (ejemplo en `seguridad_pipeline.py` líneas 18-19 o en `preprocesamiento_seguro.py`).
- **Limpieza de datos**: Elimina NA solo en columnas críticas: `['temp', 'humidity', 'windspeed', 'demand']` (línea 22 en `seguridad_pipeline.py` o en `cargar_dataframe_limpio`).
- **Split seguro**: Siempre `train_test_split` antes de cualquier transformación (línea 27 en `seguridad_pipeline.py` o en `preparar_matrices`).
- **Escalado sin fuga**: `scaler.fit_transform(X_train)` seguido de `scaler.transform(X_test)` (líneas 32-33 en `seguridad_pipeline.py` o en `preparar_matrices`).
- **Entrenamiento de modelos**: Usa funciones del módulo `ml_pipeline_e2e_practica.preprocesamiento_seguro` para preparar datos (ver `train_regression.py` y `train_classification.py`).
- **Documentación**: Comentarios en español explicando cada paso de prevención de fuga.

## Dependencias y Integraciones
- **Herramientas**: `uv` para gestión de dependencias (Python ≥3.14), no uses `pip` directamente.
- **Librerías clave**: `pandas` para manipulación, `scikit-learn` para preprocessing/ML, `numpy` para arrays.
- **Datos**: Datos originales en `data/`, datos cacheables o generados (recopilables desde el origen) en `.cache/`; si hay APIs externas ni bases de datos.

## Proyecto MLOps (Acciones Data)
Este módulo (`acciones-data`) enseña Tracking, Despliegue y Monitoreo.

### Arquitectura MLOps
- **Orquestador**: `acciones-data/src/acciones_data/pipeline_completo.py` coordina todo el flujo.
- **Datos**: NO usa `data/`. Usa `.cache/` para simular Data Lake (Raw/Silver) y Model Registry.
- **Sectores**: El sistema maneja múltiples contextos (`tecnologia`, `consumo`) dinámicamente.

### Patrones MLOps Implementados
1.  **Monitoring (Gatekeeper)**: `monitoreo_drift.py` verifica estadísticas antes de entrenar/predecir. Si hay drift (>20%), alerta.
2.  **Model Registry (Simulado)**: `entrenar_autots.py` guarda `best_model_template.csv` en `.cache/modelos/{sector}/`.
3.  **Model Routing**: `predecir_forecast.py` detecta el sector de los datos entrantes y carga el template correspondiente automáticamente.
4.  **Configuración Centralizada**: `configurar_forecast.py` define métricas y sectores.

### Comandos MLOps
- Ejecutar pipeline completo: `uv run acciones-data/src/acciones_data/pipeline_completo.py`
- Verificar drift manualmente: `uv run acciones-data/src/acciones_data/monitoreo_drift.py`

## Ejemplos de Patrones
- Para features temporales: `df['hour'] = df['timestamp'].dt.hour` (ver `seguridad_pipeline.py` o `preprocesamiento_seguro.py`).
- Para split: `train_test_split(X, y, test_size=0.2, random_state=42)` (línea 27 en `seguridad_pipeline.py` o en `preparar_matrices`).
- Para escalado seguro: Ajusta solo en train, transforma ambos sets (líneas 32-33 en `seguridad_pipeline.py` o en `preparar_matrices`).
- Para cargar datos limpios: `df = cargar_dataframe_limpio()` (ver `train_regression.py`).
- Para preparar matrices escaladas: `X_train, X_test, y_train, y_test = preparar_matrices(df)` (ver `train_regression.py` y `train_classification.py`).

Mantén la consistencia en español y enfócate en prácticas seguras contra data leakage.