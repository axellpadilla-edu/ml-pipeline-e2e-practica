"""Script para descargar datos de precios de acciones usando yfinance."""

from pathlib import Path
import yfinance as yf
from acciones_data.configurar_forecast import obtener_configuracion_sectores


def descargar_datos_sector(sector: str, tickers: list, directorio_base: Path) -> None:
    """
    Descarga los precios de cierre para un sector específico.

    Args:
        sector: Nombre del sector (ej. 'tecnologia', 'consumo')
        tickers: Lista de símbolos de acciones
        directorio_base: Ruta base donde guardar los datos (.cache/cargados)
    """
    directorio_destino = directorio_base / sector
    directorio_destino.mkdir(parents=True, exist_ok=True)

    print(f"\nDescargando sector: {sector.upper()}")
    print(f"Tickers: {tickers}")
    print(f"Destino: {directorio_destino}")

    try:
        # Descargar el precio de CIERRE de los últimos 5 años
        posible_df = yf.download(tickers, period="5y")
        if posible_df is None or posible_df.empty:
            raise RuntimeError(f"No se descargaron datos para {sector}")
        df_productos = posible_df["Close"]
    except Exception as e:
        raise RuntimeError(f"Error descargando {sector}: {e}") from e

    # Guardar a CSV
    archivo_csv = directorio_destino / f"precios_{sector}.csv"
    df_productos.to_csv(archivo_csv)

    print(f"✓ Descarga de {sector} completada.")
    print(f"  Archivo: {archivo_csv}")
    print(f"  Dimensiones: {df_productos.shape}")


def main() -> None:
    """Punto de entrada principal."""
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    directorio_base = ruta_proyecto_raiz / ".cache" / "cargados"

    print(f"Proyecto raíz: {ruta_proyecto_raiz}")
    print(f"Directorio base: {directorio_base}\n")

    sectores = obtener_configuracion_sectores()

    for sector, tickers in sectores.items():
        descargar_datos_sector(sector, tickers, directorio_base)


if __name__ == "__main__":
    main()
