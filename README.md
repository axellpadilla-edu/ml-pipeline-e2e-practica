## Taller: Data Science sin Data Leakage

Este repositorio está listo para usarse dentro de GitHub Codespaces y demuestra cómo aplicar la regla de oro _"Divide antes, transforma después"_ para prevenir fugas de información al trabajar con el dataset público **Bike Sharing Demand**.

### 1. Abrir el entorno en Codespaces

1. Haz clic en **Code ▸ Codespaces ▸ Create codespace on main** dentro de GitHub.
2. El contenedor se construirá usando Python **3.14** y la herramienta de dependencias **uv** gracias a la configuración de `.devcontainer/`.
3. Una vez que el Codespace esté listo, el comando `uv sync` se ejecutará automáticamente para instalar las dependencias.

### 2. Dependencias con uv

Si necesitas reinstalar o sincronizar dependencias manualmente, desde la raíz del proyecto ejecuta:

```bash
uv sync
```

### 3. Ejecutar el pipeline seguro

Usa `uv run` para mantener un entorno reproducible:

```bash
uv run src/seguridad_pipeline.py
```

#### Experimentos adicionales

```bash
# Para ejecutar el experimento de Regresión
uv run src/train_regression.py

# Para ejecutar el experimento de Clasificación
uv run src/train_classification.py
```

### 4. Pipeline independiente de anonimización (nuevo demo)

El script `src/pipeline_anonimizacion.py` está pensado para la práctica **Anonimización de Datos (30 min)**. Ejecuta:

```bash
uv run src/pipeline_anonimizacion.py
```

Pasos que se realizan en vivo:

1. **Generación de datos ficticios** con [Faker](https://faker.readthedocs.io/) (IDs, documento nacional, dirección detallada, asesor, monto, etc.).
2. **Enriquecimiento temporal** (`mes`, `anio`, `es_fin_de_semana`) sin duplicar lógica entre scripts.
3. **Anonimización en tres capas**, únicamente con el paquete interno `anonimizar-datos`:
    - Hash SHA-256 (irreversible) para `cliente_id`.
    - Enmascarado parcial para `documento_nacional`.
    - Tokenización reversible para `direccion_detallada` y `asesor_venta`, guardando los diccionarios en `.cache/anonimizacion/tokenizacion.json`.
4. **Evidencia reproducible**: se guardan los CSV `dataset_original.csv` y `dataset_anonimo.csv` en `.cache/anonimizacion/` para comparar antes/después en demos o notebooks.

> Este pipeline no depende de archivos en `data/`; todos los registros se generan al vuelo, permitiendo explicar por qué la anonimización debe suceder antes de compartir los datos.

### 4. Estructura principal

```
.
├── main.py                          # Script de ejemplo simple
├── pyproject.toml                   # Configuración de dependencias con uv
├── README.md                        # Este archivo
├── data/
│   └── bike_sharing_demand.csv      # Muestra ligera del dataset público de Bike Sharing Demand
├── src/
│   ├── seguridad_pipeline.py        # Script principal que aplica la regla "Divide antes, transforma después"
│   ├── pipeline_anonimizacion.py    # Crea datos sintéticos (Faker) y aplica hashing/masking/tokenización
│   ├── train_regression.py          # Experimento de regresión para predicción de demanda
│   ├── train_classification.py      # Experimento de clasificación (ej. demanda alta/baja)
│   └── ml_pipeline_e2e_practica/
│       ├── __init__.py
│       └── preprocesamiento_seguro.py  # Módulo de preprocesamiento seguro contra data leakage
└── notebooks/
    ├── demo_codigo_seguro.ipynb     # Versión interactiva del pipeline seguro
    └── demo_comparativa_modelos.ipynb  # Comparación de modelos con y sin prevención de fuga
```

### 5. Descripción de componentes clave

- **seguridad_pipeline.py**: Implementa el flujo completo de carga, limpieza, extracción de features, split seguro y escalado sin fuga.
- **preprocesamiento_seguro.py**: Contiene funciones reutilizables para preprocesamiento que evita data leakage.
- **train_regression.py** y **train_classification.py**: Scripts para entrenar modelos de regresión y clasificación, demostrando la importancia del split antes de transformación.
- **demo_codigo_seguro.ipynb**: Notebook interactivo para seguir el proceso paso a paso.
- **demo_comparativa_modelos.ipynb**: Compara resultados de modelos entrenados correctamente vs. con fuga de datos.

### 6. Notebook interactivo

Abre `notebooks/demo_codigo_seguro.ipynb` para seguir el flujo paso a paso, desde la carga de datos hasta la estandarización segura con `StandardScaler`.

Abre `notebooks/demo_comparativa_modelos.ipynb` para ver una comparación práctica de cómo la fuga de datos afecta el rendimiento de los modelos.

---

> **Nota:** El archivo `data/bike_sharing_demand.csv` contiene una muestra reducida del dataset original disponible públicamente en Kaggle. Inclúyelo únicamente para fines educativos durante el taller.

---

## Taller: MLOps con Forecasting de Acciones

Este repositorio incluye un segundo módulo (`acciones-data`) diseñado para enseñar conceptos de **MLOps** (Machine Learning Operations) aplicados a un problema de series temporales financieras.

### 1. Conceptos Clave
- **Tracking**: Registro de experimentos y modelos ganadores usando AutoTS.
- **Model Registry (Simulado)**: Almacenamiento versionado de artefactos (templates) en `.cache/modelos`.
- **Despliegue & Routing**: Inferencia condicional que selecciona el modelo adecuado según el sector (Tecnología vs. Consumo).
- **Monitoreo**: Detección de *Data Drift* antes de permitir la ejecución del pipeline.

### 2. Ejecución del Pipeline MLOps

El pipeline completo orquesta la descarga, transformación, monitoreo, entrenamiento e inferencia.

```bash
uv run acciones-data/src/acciones_data/pipeline_completo.py
```

### 3. Estructura de Datos (Simulación Data Lake)
A diferencia del demo de Bike Sharing, este pipeline **no usa la carpeta `data/`**. Simula un entorno productivo usando `.cache/` como almacenamiento temporal/externo:

- `.cache/cargados/`: Datos crudos (Raw).
- `.cache/transformados/`: Datos procesados (Silver).
- `.cache/modelos/`: Artefactos de modelos (Registry).
- `.cache/predicciones/`: Resultados finales.

### 4. Presentación
Consulta `MLOps_Presentation.md` para la guía teórica y el walkthrough del taller.
