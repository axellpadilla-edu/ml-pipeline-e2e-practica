"""
Script para transformar datos de acciones.

Estrategia: Series Temporales Múltiples Independientes (con soporte global opcional)
------------------------------------------------------------------------------------
En este enfoque simplificado, mantenemos el DataFrame en formato 'Wide' (Ancho)
donde cada columna es una serie temporal independiente (un precio de acción).

Manejo de Features Exógenas (Explicación):
------------------------------------------
1. Features Globales (ej: Festivos):
   - AutoTS puede manejarlos automáticamente con el parámetro `holiday_country`.
   - Si se requieren globales personalizados (ej: Precio Petróleo), se pasan
     como `future_regressor` (deben tener valores para historia + futuro).

2. Features Específicas por Serie (ej: Tipo de Evento por Tienda):
   - AutoTS no soporta nativamente diccionarios de features por serie.
   - Estrategia recomendada: One-Hot Encoding + Future Regressor.
     a. Convertir variables categóricas a numéricas (dummies).
     b. Aplanar todas las columnas en un único DataFrame `future_regressor`.
     c. AutoTS detectará correlaciones: aprenderá que 'Evento_Tienda_A' solo
        afecta a 'Ventas_Tienda_A' y no a 'Ventas_Tienda_B'.

En este script, nos limitamos a limpiar y validar los precios (Targets),
dejando que AutoTS maneje festivos y estacionalidades internamente.
"""

from pathlib import Path
import pandas as pd


def cargar_datos_acciones(ruta_csv: Path) -> pd.DataFrame:
    """
    Carga el CSV de precios de cierre históricos.

    Args:
        ruta_csv: Ruta al archivo CSV.

    Returns:
        DataFrame con precios de cierre.
    """
    df = pd.read_csv(ruta_csv, index_col=0, parse_dates=True)
    print(f"Datos cargados: {df.shape[0]} filas, {df.shape[1]} columnas")
    print(f"Período: {df.index.min()} a {df.index.max()}")
    return df


def asegurar_formato_autots(df: pd.DataFrame) -> pd.DataFrame:
    """
    Valida y asegura que el DataFrame cumpla con los requisitos de AutoTS.

    Requisitos:
    1. Índice de tipo DatetimeIndex.
    2. Ordenado cronológicamente.

    Args:
        df: DataFrame con features.

    Returns:
        DataFrame formateado y validado.
    """
    df_autots = df.copy()

    # Asegurar índice datetime
    if not isinstance(df_autots.index, pd.DatetimeIndex):
        df_autots.index = pd.to_datetime(df_autots.index)

    # Ordenar por fecha (crítico para series temporales)
    df_autots = df_autots.sort_index()

    # Inferir frecuencia para feedback visual
    if isinstance(df_autots.index, pd.DatetimeIndex):
        freq = pd.infer_freq(df_autots.index)
        print(f"Formato validado para AutoTS. Frecuencia inferida: {freq}")
    else:
        print("Advertencia: El índice no es DatetimeIndex, AutoTS podría fallar.")

    return df_autots


def guardar_datos_transformados(df: pd.DataFrame, directorio_destino: Path) -> None:
    """
    Guarda el DataFrame transformado en un CSV.

    Args:
        df: DataFrame a guardar.
        directorio_destino: Directorio donde guardar.
    """
    directorio_destino.mkdir(parents=True, exist_ok=True)
    archivo_csv = directorio_destino / "precios_cierre_acciones_transformado.csv"

    try:
        df.to_csv(archivo_csv)
        print(f"Datos transformados guardados en: {archivo_csv}")
    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        raise


def main() -> None:
    """Punto de entrada principal."""
    # Configuración de rutas
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    ruta_csv = (
        ruta_proyecto_raiz
        / ".cache"
        / "cargados"
        / "acciones"
        / "precios_cierre_acciones.csv"
    )
    directorio_destino = ruta_proyecto_raiz / ".cache" / "transformados" / "acciones"

    print(f"Proyecto raíz: {ruta_proyecto_raiz}")
    print(f"Archivo fuente: {ruta_csv}")
    print(f"Directorio destino: {directorio_destino}\n")

    # 1. Cargar datos originales
    df = cargar_datos_acciones(ruta_csv)

    # 2. Validación de formato (Sin agregar features técnicas complejas)
    df_autots = asegurar_formato_autots(df)

    # 3. Guardar resultado
    guardar_datos_transformados(df_autots, directorio_destino)

    print("\n✓ Transformación completada exitosamente")


if __name__ == "__main__":
    main()
