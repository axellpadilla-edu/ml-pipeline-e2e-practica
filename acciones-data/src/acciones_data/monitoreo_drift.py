"""
Script para monitorear Data Drift en los datos de acciones.

Este script simula un sistema de monitoreo comparando estadísticas de datos recientes
("producción") contra datos históricos ("referencia").
"""

from pathlib import Path
import pandas as pd
from acciones_data.configurar_forecast import (
    cargar_datos_transformados,
    obtener_configuracion_sectores,
)


def detectar_drift(
    df: pd.DataFrame, ventana_reciente: int = 30, umbral_alerta: float = 0.20
) -> bool:
    """
    Detecta si hay drift significativo en los datos recientes comparados con el histórico.

    Args:
        df: DataFrame con los datos.
        ventana_reciente: Número de días a considerar como "datos recientes".
        umbral_alerta: Porcentaje de cambio permitido antes de lanzar alerta (0.20 = 20%).

    Returns:
        True si se detecta drift, False si todo está normal.
    """
    print(f"\nAnalizando Data Drift (Ventana reciente: {ventana_reciente} días)...")

    # Separar referencia (histórico) y actual (reciente)
    df_actual = df.tail(ventana_reciente)
    df_referencia = df.iloc[:-ventana_reciente]

    drift_detectado = False

    for columna in df.columns:
        # Calcular estadísticas
        media_ref = df_referencia[columna].mean()
        media_act = df_actual[columna].mean()

        std_ref = df_referencia[columna].std()
        std_act = df_actual[columna].std()

        # Calcular cambio porcentual en la media
        if media_ref != 0:
            cambio_media = abs((media_act - media_ref) / media_ref)
        else:
            cambio_media = 0.0

        print(f"\n  Variable: {columna}")
        print(
            f"    Media Ref: {media_ref:.4f} (Std: {std_ref:.4f}) | Media Act: {media_act:.4f} (Std: {std_act:.4f})"
        )
        print(f"    Cambio Media: {cambio_media:.2%}")

        # Regla simple de detección
        if cambio_media > umbral_alerta:
            print(
                f"    ⚠️ ALERTA: Drift detectado en {columna} (Cambio > {umbral_alerta:.0%})"
            )
            drift_detectado = True
        else:
            print("    ✅ Estado: Normal")

    return drift_detectado


def monitorear_sector(sector: str, ruta_raiz: Path) -> None:
    """Monitorea drift para un sector específico."""
    ruta_datos = (
        ruta_raiz
        / ".cache"
        / "transformados"
        / sector
        / f"precios_{sector}_transformado.csv"
    )

    print(f"\n{'=' * 40}")
    print(f"MONITOREANDO SECTOR: {sector.upper()}")
    print(f"{'=' * 40}")

    if not ruta_datos.exists():
        print(f"⚠️ Datos no encontrados: {ruta_datos}")
        return

    # Cargar datos
    df = cargar_datos_transformados(ruta_datos)

    # Ejecutar monitoreo
    hay_drift = detectar_drift(df)

    if hay_drift:
        print(
            f"\n⚠️ ADVERTENCIA GLOBAL ({sector}): Se han detectado cambios significativos."
        )
    else:
        print(f"\n✅ MONITOREO EXITOSO ({sector}): Datos estables.")


def main():
    # Rutas
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    sectores = obtener_configuracion_sectores()

    for sector in sectores:
        monitorear_sector(sector, ruta_proyecto_raiz)


if __name__ == "__main__":
    main()
