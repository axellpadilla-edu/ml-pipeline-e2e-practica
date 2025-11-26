"""Script para entrenar y comparar modelos de forecasting con AutoTS."""

from pathlib import Path
import pandas as pd
import joblib  # type: ignore
from autots import AutoTS

# Importar funciones del módulo de configuración
from acciones_data.configurar_forecast import (
    cargar_datos_transformados,
    definir_configuracion_forecast,
    inicializar_autots,
)
from acciones_data.utils import suppress_output


def entrenar_modelo(model: AutoTS, df: pd.DataFrame) -> AutoTS:
    """
    Entrena el modelo AutoTS con los datos.

    Args:
        model: Instancia de AutoTS
        df: DataFrame con datos

    Returns:
        Modelo entrenado
    """
    print("\nIniciando entrenamiento...")
    # Suprimir logs de AutoTS durante el entrenamiento
    with suppress_output():
        model = model.fit(df)
    print("Entrenamiento completado.")
    return model


def mostrar_resultados(model: AutoTS) -> None:
    """
    Muestra los resultados del entrenamiento: mejor modelo, métricas, etc.

    Args:
        model: Modelo entrenado
    """
    print("\n" + "=" * 50)
    print("RESULTADOS DEL ENTRENAMIENTO")
    print("=" * 50)

    # Obtener resultados
    results = model.results()

    if isinstance(results, str):
        print(f"Error en entrenamiento: {results}")
        return

    # Mejor modelo
    print(f"Mejor modelo encontrado: {model.best_model_name}")

    # Obtener score del mejor modelo
    try:
        best_score = results.loc[results["ID"] == model.best_model_id, "Score"].iloc[0]
        print(f"Métrica de validación (Score): {best_score:.4f}")
    except Exception:
        print("No se pudo obtener el score del mejor modelo.")

    print(f"\nTotal de modelos evaluados: {len(results)}")

    # Top 5 modelos
    print("\nTop 5 modelos por score (menor es mejor):")
    # AutoTS Score es una pérdida ponderada, así que MENOR es MEJOR.
    top_models = results.nsmallest(5, "Score")

    for idx, row in top_models.iterrows():
        print(
            f"  {row['Model']} - Score: {row['Score']:.4f} - SMAPE: {row.get('smape', 'N/A')}"
        )

    # Mostrar mejores modelos por serie (Horizontal Ensemble)
    try:
        print("\nMejores modelos por serie (Horizontal Ensemble):")
        params = model.best_model_params
        series_dict = params.get("series", {})
        models_dict = params.get("models", {})

        if series_dict:
            for series_name, model_id in series_dict.items():
                model_info = models_dict.get(model_id, {})
                model_name = model_info.get("Model", "Unknown")
                print(f"  {series_name}: {model_name}")
        else:
            print(
                "  No se encontró desglose por serie (posiblemente se eligió un modelo global)."
            )

    except Exception as e:
        print(f"  No se pudo obtener la información por serie: {e}")

    print("\nModelo AutoTS entrenado exitosamente.")


def guardar_modelo(model: AutoTS, directorio_destino: Path) -> None:
    """
    Guarda el modelo entrenado usando joblib y exporta la plantilla del mejor modelo.

    Args:
        directorio_destino: Directorio donde guardar
        model: Modelo a guardar
    """
    directorio_destino.mkdir(parents=True, exist_ok=True)

    # 1. Guardar objeto completo (para uso inmediato/interactivo)
    ruta_modelo = directorio_destino / "modelo_autots.pkl"
    joblib.dump(model, ruta_modelo)
    print(f"Modelo completo guardado en: {ruta_modelo}")

    # 2. Exportar plantilla (best practice para producción/reproducibilidad)
    # Permite re-entrenar solo los mejores modelos en el futuro o en otro entorno
    # Usamos .csv porque .json requiere índices únicos que AutoTS no siempre garantiza en el template
    ruta_template = directorio_destino / "best_model_template.csv"
    model.export_template(
        str(ruta_template),
        models="best",
        n=15,  # Exportar los top 15 modelos para tener variedad en el ensemble
        max_per_model_class=5,
    )
    print(f"Plantilla del mejor modelo exportada a: {ruta_template}")


from acciones_data.configurar_forecast import obtener_configuracion_sectores


def entrenar_sector(sector: str, ruta_raiz: Path) -> None:
    """Entrena modelo para un sector específico."""
    ruta_csv = (
        ruta_raiz
        / ".cache"
        / "transformados"
        / sector
        / f"precios_{sector}_transformado.csv"
    )
    directorio_modelo = ruta_raiz / ".cache" / "modelos" / sector

    print(f"\n{'=' * 40}")
    print(f"ENTRENANDO SECTOR: {sector.upper()}")
    print(f"{'=' * 40}")

    if not ruta_csv.exists():
        print(f"⚠️ Archivo no encontrado: {ruta_csv}")
        return

    # Cargar datos
    df = cargar_datos_transformados(ruta_csv)

    # Configuración
    configuracion = definir_configuracion_forecast()

    # Inicializar y Entrenar
    model = inicializar_autots(configuracion, df)
    model_entrenado = entrenar_modelo(model, df)

    # Resultados y Guardado
    mostrar_resultados(model_entrenado)
    guardar_modelo(model_entrenado, directorio_modelo)
    print(f"✓ Entrenamiento de {sector} completado.")


def main() -> None:
    """Punto de entrada principal."""
    ruta_proyecto_raiz = Path(__file__).resolve().parent.parent.parent.parent
    print(f"Proyecto raíz: {ruta_proyecto_raiz}\n")

    sectores = obtener_configuracion_sectores()

    for sector in sectores:
        entrenar_sector(sector, ruta_proyecto_raiz)


if __name__ == "__main__":
    main()
