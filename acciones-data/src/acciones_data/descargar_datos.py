"""Script para descargar datos de precios de acciones de tecnología usando yfinance."""

from pathlib import Path
import yfinance as yf


def descargar_datos_acciones(directorio_destino: Path) -> None:
    """
    Descarga los precios de cierre de acciones de tecnología usando yfinance.

    Args:
        directorio_destino: Ruta donde guardar el archivo CSV descargado

    Raises:
        RuntimeError: Si la descarga falla
    """
    directorio_destino.mkdir(parents=True, exist_ok=True)

    # 1. Definir los "productos" (5 acciones de tecnología)
    tickers_productos = ["TSLA", "MSFT", "GOOGL", "AMZN", "NVDA"]

    print("Descargando precios de cierre de acciones de tecnología...")
    print(f"Tickers: {tickers_productos}")
    print(f"Destino: {directorio_destino}")

    try:
        # 2. Descargar el precio de CIERRE de los últimos 5 años
        posible_df = yf.download(tickers_productos, period="5y")
        if posible_df is None or posible_df.empty:
            raise RuntimeError("No se descargaron datos; el DataFrame está vacío.")
        df_productos = posible_df["Close"]
    except Exception as e:
        raise RuntimeError(f"Error durante la descarga desde Yahoo Finance: {e}") from e

    # Guardar a CSV
    archivo_csv = directorio_destino / "precios_cierre_acciones.csv"
    df_productos.to_csv(archivo_csv)

    print("\n✓ Descarga completada exitosamente")
    print(f"  Archivo guardado: {archivo_csv}")
    print(
        f"  Dimensiones: {df_productos.shape[0]} filas, {df_productos.shape[1]} columnas"
    )
    print("Período: últimos 5 años")
    print(
        f"  Datos desde: {df_productos.index.min()} hasta: {df_productos.index.max()}"
    )


def main() -> None:
    """Punto de entrada principal."""
    # Obtener ruta raíz del proyecto principal
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    directorio_destino = ruta_proyecto_raiz / ".cache" / "cargados" / "acciones"

    print(f"Proyecto raíz: {ruta_proyecto_raiz}")
    print(f"Directorio de destino: {directorio_destino}\n")

    descargar_datos_acciones(directorio_destino)


if __name__ == "__main__":
    main()
