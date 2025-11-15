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
