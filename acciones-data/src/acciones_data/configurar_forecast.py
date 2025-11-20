"""Script para configurar métricas y longitud de predicción para forecasting de acciones con AutoTS."""

from pathlib import Path
import pandas as pd
from autots import AutoTS


def cargar_datos_transformados(ruta_csv: Path) -> pd.DataFrame:
    """
    Carga el CSV de datos transformados.

    Args:
        ruta_csv: Ruta al archivo CSV transformado

    Returns:
        DataFrame con datos transformados
    """
    df = pd.read_csv(ruta_csv, index_col=0, parse_dates=True)
    print(f"Datos transformados cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(f"Período: {df.index.min()} a {df.index.max()}")
    return df


def definir_configuracion_forecast() -> dict:
    """
    Define la configuración para el forecasting: métricas y longitud de predicción.

    Returns:
        Diccionario con configuración
    """
    # Definir métricas de evaluación
    metricas = [
        "smape",
        "mae",
        "rmse",
        "made",
    ]  # SMAPE, MAE, RMSE, Mean Absolute Deviation Error

    # Definir longitud de predicción (forecast length)
    forecast_length = 30  # Predecir 30 días adelante

    configuracion = {"metricas": metricas, "forecast_length": forecast_length}

    print("Configuración definida:")
    print(f"  Métricas: {metricas}")
    print(f"  Longitud de predicción: {forecast_length} días")

    return configuracion


def inicializar_autots(configuracion: dict, df: pd.DataFrame) -> AutoTS:
    """
    Inicializa el modelo AutoTS con la configuración definida.

    Args:
        configuracion: Diccionario con métricas y forecast_length
        df: DataFrame con datos

    Returns:
        Instancia de AutoTS configurada
    """
    # Configuración optimizada para DevContainers/Codespaces (rápida)
    model = AutoTS(
        forecast_length=configuracion["forecast_length"],
        frequency="infer",  # Inferir frecuencia (diaria, mensual, etc.)
        prediction_interval=0.9,  # Intervalo de confianza del 90%
        holiday_country="US",  # Agregar festivos de US automáticamente como features globales
        # --- Configuración de Modelos y Velocidad ---
        # 'simple': Un modelo para todas las series.
        # 'horizontal-max': Un modelo distinto para cada serie (el mejor para cada una).
        ensemble="horizontal-max",
        model_list="superfast",  # Lista de modelos muy rápida para pruebas.
        # Opciones: "superfast", "fast", "default", "all", "probabilistic", "multivariate", o una lista ['ARIMA', 'ETS']
        # transformer_list="fast",  # Transformaciones rápidas. Opciones: "superfast", "fast", "all"
        # --- Configuración de Búsqueda (Algoritmo Genético) ---
        max_generations=1,  # Número de generaciones del algoritmo genético.
        # 1-5 para pruebas rápidas, 10-20+ para producción.
        num_validations=1,  # Número de validaciones cruzadas (backtesting).
        # 0-1 para velocidad, 2+ para robustez.
        validation_method="backwards",  # Método de validación: "backwards" (ventana rodante), "even", "similarity", "seasonal"
        # --- Métricas ---
        metric_weighting={
            "smape_weighting": 2,  # Peso mayor para SMAPE (Symmetric Mean Absolute Percentage Error)
            "mae_weighting": 1,
            "rmse_weighting": 1,
            "made_weighting": 1,
        },
        # --- Otros ---
        drop_most_recent=0,  # Si se deben ignorar los datos más recientes (útil si están incompletos)
        n_jobs=1,  # Paralelismo: 1 proceso para evitar sobrecarga en devcontainer.
        verbose=0,  # Nivel de detalle en logs (0=silencio, 1=info, 2=debug)
    )

    print("Modelo AutoTS inicializado con configuración rápida (DevContainer):")
    print(f"  Forecast length: {configuracion['forecast_length']}")
    print("  Ensemble: 'horizontal-max'")
    print("  Model list: superfast")
    print("  Max generations: 1")

    return model


def main() -> None:
    """Punto de entrada principal."""
    # Obtener ruta raíz del proyecto principal
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    ruta_csv = (
        ruta_proyecto_raiz
        / ".cache"
        / "transformados"
        / "acciones"
        / "precios_cierre_acciones_transformado.csv"
    )

    print(f"Proyecto raíz: {ruta_proyecto_raiz}")
    print(f"Archivo de datos transformados: {ruta_csv}\n")

    # Cargar datos transformados
    df = cargar_datos_transformados(ruta_csv)

    # Definir configuración
    configuracion = definir_configuracion_forecast()

    # Inicializar AutoTS
    model = inicializar_autots(configuracion, df)

    print(f"Modelo AutoTS inicializado: {type(model)}")
    print("\n✓ Configuración completada exitosamente")
    print("El modelo AutoTS está listo para entrenamiento.")


if __name__ == "__main__":
    main()
