"""
Script orquestador para ejecutar el pipeline completo de predicción de acciones.

Este script coordina la ejecución secuencial de los módulos del proyecto:
1. Descarga de datos (Yahoo Finance)
2. Transformación y limpieza
3. Entrenamiento (AutoTS) y generación de Template
4. Inferencia (Predicción) usando el Template

Uso:
    uv run acciones-data/src/acciones_data/pipeline_completo.py
"""

import sys
import time
from acciones_data import descargar_datos
from acciones_data import transformar_datos
from acciones_data import monitoreo_drift
from acciones_data import entrenar_autots
from acciones_data import predecir_forecast


def ejecutar_paso(nombre_paso, funcion_main):
    """
    Ejecuta una función main() de un módulo midiendo el tiempo y manejando errores.
    """
    print(f"\n{'=' * 80}")
    print(f"🚀 INICIANDO PASO: {nombre_paso}")
    print(f"{'=' * 80}")

    start_time = time.time()
    try:
        funcion_main()
        elapsed = time.time() - start_time
        print(
            f"\n✅ PASO '{nombre_paso}' COMPLETADO EXITOSAMENTE en {elapsed:.2f} segundos."
        )
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO en PASO '{nombre_paso}': {e}")
        print("El pipeline se ha detenido debido a un error.")
        sys.exit(1)


def main():
    print("\n" + "*" * 80)
    print("🤖 INICIANDO PIPELINE E2E DE FORECASTING DE ACCIONES")
    print("*" * 80)

    total_start_time = time.time()

    # Paso 1: Descarga
    # Descarga los datos más recientes desde Yahoo Finance
    ejecutar_paso("1. Descarga de Datos Históricos", descargar_datos.main)

    # Paso 2: Transformación
    # Prepara los datos para AutoTS (formato Wide, limpieza básica)
    ejecutar_paso("2. Transformación y Preparación de Datos", transformar_datos.main)

    # Paso 3: Monitoreo
    # Verifica si hay Data Drift antes de continuar
    ejecutar_paso("3. Monitoreo de Data Drift", monitoreo_drift.main)

    # Paso 4: Entrenamiento
    # Entrena modelos (o actualiza el template) con los datos transformados.
    # Genera 'best_model_template.json'
    ejecutar_paso(
        "4. Entrenamiento y Generación de Template (AutoTS)", entrenar_autots.main
    )

    # Paso 5: Predicción
    # Usa el template generado para predecir el futuro sin re-entrenar desde cero.
    ejecutar_paso(
        "5. Generación de Pronóstico (Inferencia Producción)", predecir_forecast.main
    )

    total_elapsed = time.time() - total_start_time
    print(f"\n{'*' * 80}")
    print(f"✨ PIPELINE COMPLETADO EXITOSAMENTE en {total_elapsed:.2f} segundos.")
    print(f"{'*' * 80}\n")


if __name__ == "__main__":
    main()
