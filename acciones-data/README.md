# M5 Forecast

Paquete para descargar y gestionar datos del dataset **M5 Forecasting Accuracy** desde Kaggle.

## Descripción

Este paquete facilita la descarga automática de los datos de la competencia M5 Forecasting Accuracy en Kaggle, extrayéndolos en el directorio `.cache/cargados/m5-forecast` del proyecto principal para mantener la separación entre datos originales y datos cacheables.

## Requisitos

- Cuenta de Kaggle activa
- API key de Kaggle configurada en `.env`
- ~5GB de espacio en disco

## Configuración

1. **Obtener credenciales de Kaggle**:
   - Ve a https://www.kaggle.com/account/settings/account
   - Haz clic en "Create New Token"
   - Se descargará `kaggle.json` con tus credenciales

2. **Configurar `.env`**:
   - Copia el contenido de `.env.example` a `.env`
   - Extrae `username` y `key` del archivo `kaggle.json` descargado
   - Completa los valores en `.env`:
     ```
     KAGGLE_USERNAME=tu_usuario
     KAGGLE_KEY=tu_api_key
     ```

## Uso

Para descargar los datos del competencia M5:

```bash
uv run -m m5_forecast.descargar_datos
```

O directamente desde Python:

```python
from pathlib import Path
from m5_forecast.descargar_datos import descargar_datos_m5

directorio_destino = Path(".cache/cargados/m5-forecast")
descargar_datos_m5(directorio_destino)
```

## Archivos descargados

El script descargará y extraerá:

- `sales_train_validation.csv`: Datos históricos de ventas (~1.9GB)
- `calendar.csv`: Información de calendario y eventos (~2MB)
- `sell_prices.csv`: Precios de venta por semana (~400MB)
- `sample_submission.csv`: Formato de envío de predicciones (~300MB)

## Notas

- Los datos se guardan en `.cache/cargados/m5-forecast` para diferenciar entre datos originales (en `data/`) y datos cacheables (en `.cache/`)
- El directorio `.cache/` está incluido en `.gitignore` para no subir archivos grandes al repositorio
- La descarga es unidireccional; si necesitas limpiar, simplemente elimina el directorio `.cache/cargados/m5-forecast`
