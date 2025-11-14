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
data/
	bike_sharing_demand.csv        # Muestra ligera del dataset público
src/
	seguridad_pipeline.py          # Script que aplica la regla "Divide antes, transforma después"
notebooks/
	demo_codigo_seguro.ipynb       # Versión interactiva de los mismos pasos
.devcontainer/                   # Configuración de Codespaces (Python 3.14 + uv)
```

### 5. Notebook interactivo

Abre `notebooks/demo_codigo_seguro.ipynb` para seguir el flujo paso a paso, desde la carga de datos hasta la estandarización segura con `StandardScaler`.

---

> **Nota:** El archivo `data/bike_sharing_demand.csv` contiene una muestra reducida del dataset original disponible públicamente en Kaggle. Inclúyelo únicamente para fines educativos durante el taller.
