"""
Script para generar pronósticos utilizando un modelo AutoTS entrenado (vía template).

Este script demuestra el flujo de producción:
1. Cargar nuevos datos (o los históricos actualizados).
2. Cargar la plantilla del mejor modelo seleccionado en entrenamiento.
3. Re-entrenar (Fit) rápidamente solo ese modelo con los datos actuales.
4. Generar el pronóstico futuro.
"""

from pathlib import Path

import pandas as pd
from autots import AutoTS

# Importar funciones de configuración
from acciones_data.configurar_forecast import (
    cargar_datos_transformados,
    definir_configuracion_forecast,
)
from acciones_data.utils import suppress_output


def cargar_template(ruta_template: Path) -> str:
    """
    Verifica que el template exista y devuelve su ruta como string.
    """
    if not ruta_template.exists():
        raise FileNotFoundError(f"No se encontró el template en: {ruta_template}")
    return str(ruta_template)


def generar_pronostico(
    df: pd.DataFrame, ruta_template: str, forecast_length: int
) -> pd.DataFrame:
    """
    Genera el pronóstico usando el template.

    Args:
        df: Datos históricos.
        ruta_template: Ruta al archivo JSON del template.
        forecast_length: Días a predecir.

    Returns:
        DataFrame con las predicciones.
    """
    print(f"\nCargando template desde: {ruta_template}")
    print(f"Datos históricos disponibles hasta: {df.index.max()}")
    print(f"Generando pronóstico para los próximos {forecast_length} días...")

    # Inicializar AutoTS para inferencia
    # Clave: max_generations=0 para solo correr el modelo del template sin buscar nuevos
    # Se pasa import_template directamente al constructor si la versión lo soporta,
    # o se usa el método después. Siguiendo la instrucción del usuario, lo pasamos aquí.
    # Nota: Si la versión instalada de AutoTS no soporta import_template en __init__,
    # se deberá usar model.import_template() después.
    model = AutoTS(
        forecast_length=forecast_length,
        frequency="infer",
        prediction_interval=0.9,
        ensemble="horizontal-max",  # Mantener la misma estrategia de ensemble
        model_list="superfast",  # Fallback
        max_generations=0,  # Importante: No evolucionar, solo ajustar el template
        num_validations=0,  # No necesitamos validar, solo predecir
        n_jobs=1,
        verbose=0,  # Silencioso para producción
        holiday_country="US",
    )

    # Importar el template
    # Usamos el método explícito para asegurar compatibilidad y manejo de errores
    # Referencia: https://github.com/winedarksea/AutoTS/blob/master/production_example.py
    try:
        model = model.import_template(ruta_template, method="only")
        if isinstance(model, ValueError):
            raise ValueError("El template importado no es válido.")
    except Exception as e:
        print(f"Error importando template: {e}")
        raise e

    # Ajustar (Fit) el modelo a los datos
    # Usamos fit() con max_generations=0 para que evalúe los modelos del template
    # y seleccione el mejor (o construya el ensemble) con los datos actuales.
    # Nota: model.fit_data() sería aún más rápido si ya tuviéramos un solo modelo seleccionado,
    # pero fit() es más robusto al importar una lista de candidatos (n=15).
    with suppress_output():
        model = model.fit(df)

    # Predecir
    prediction = model.predict()

    # Extraer el forecast
    forecasts_df = prediction.forecast

    print("\nPronóstico generado exitosamente.")
    return forecasts_df


def guardar_pronostico(df_forecast: pd.DataFrame, directorio_destino: Path) -> None:
    """Guarda el pronóstico en CSV."""
    directorio_destino.mkdir(parents=True, exist_ok=True)
    ruta_salida = directorio_destino / "pronostico_acciones.csv"
    df_forecast.to_csv(ruta_salida)
    print(f"Pronóstico guardado en: {ruta_salida}")


def main() -> None:
    """Flujo principal de predicción."""
    # Rutas
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    ruta_datos = (
        ruta_proyecto_raiz
        / ".cache"
        / "transformados"
        / "acciones"
        / "precios_cierre_acciones_transformado.csv"
    )
    ruta_template = (
        ruta_proyecto_raiz
        / ".cache"
        / "modelos"
        / "acciones"
        / "best_model_template.csv"
    )
    directorio_salida = ruta_proyecto_raiz / ".cache" / "predicciones" / "acciones"

    # 1. Cargar datos
    df = cargar_datos_transformados(ruta_datos)

    # 2. Obtener configuración (solo para saber el forecast_length original si se desea)
    config = definir_configuracion_forecast()
    forecast_length = config["forecast_length"]

    # 3. Generar pronóstico
    try:
        ruta_template_str = cargar_template(ruta_template)
        df_forecast = generar_pronostico(df, ruta_template_str, forecast_length)

        # 4. Mostrar y guardar
        print("\nPrimeras 5 filas del pronóstico:")
        print(df_forecast.head())
        guardar_pronostico(df_forecast, directorio_salida)

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print(
            "Por favor, ejecuta primero el script de entrenamiento para generar el template."
        )
    except Exception as e:
        print(f"\nError inesperado: {e}")


if __name__ == "__main__":
    main()
