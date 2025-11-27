"""Pipeline independiente para demostrar anonimización de datos sensibles."""

from __future__ import annotations

import json
import random
import string
from pathlib import Path
from typing import Dict, Iterable

import pandas as pd
from faker import Faker

from anonimizar_datos import (
    anonimizar_columnas_hash,
    enmascarar_columnas,
    tokenizar_columnas,
)

CACHE_DIR = Path(__file__).resolve().parent.parent / ".cache" / "anonimizacion"
CATEGORIAS = ("tecnologia", "consumo", "moda")
HASH_COLUMNS = ("cliente_id",)
MASK_COLUMNS = ("documento_nacional",)
TOKEN_COLUMNS = ("direccion_detallada", "asesor_venta")
HASH_SALT = "ml-pipeline-e2e-demo"
DEFAULT_REGISTROS = 25
FAKER_LOCALE = "es_MX"


def generar_datos_ficticios(
    n_registros: int = DEFAULT_REGISTROS,
    *,
    seed: int = 42,
) -> pd.DataFrame:
    """Crea un DataFrame con PII creíble usando Faker para el demo."""

    if n_registros <= 0:
        raise ValueError("n_registros debe ser mayor que cero.")

    faker = Faker(FAKER_LOCALE)
    faker.seed_instance(seed)
    rng = random.Random(seed)

    def _documento() -> str:
        numero = rng.randint(10_000_000, 99_999_999)
        sufijo = "".join(rng.choice(string.ascii_uppercase) for _ in range(2))
        return f"DNI{numero}{sufijo}"

    registros: list[Dict[str, object]] = []
    for consecutivo in range(1, n_registros + 1):
        fecha = faker.date_between(start_date="-120d", end_date="today")
        registros.append(
            {
                "venta_id": consecutivo,
                "cliente_id": f"CLI-{consecutivo:03d}",
                "documento_nacional": _documento(),
                "direccion_detallada": faker.address().replace("\n", ", "),
                "fecha_compra": pd.Timestamp(fecha),
                "monto_compra": round(rng.uniform(1200, 8500), 2),
                "categoria": rng.choice(CATEGORIAS),
                "asesor_venta": faker.name(),
            }
        )

    return pd.DataFrame(registros)


def enriquecer_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega features temporales sin duplicar lógica en otros scripts."""

    enriquecido = df.copy()
    enriquecido["es_fin_de_semana"] = enriquecido["fecha_compra"].dt.dayofweek >= 5
    enriquecido["mes"] = enriquecido["fecha_compra"].dt.month
    enriquecido["anio"] = enriquecido["fecha_compra"].dt.year
    return enriquecido


def aplicar_anonimizacion(
    df: pd.DataFrame,
) -> tuple[pd.DataFrame, Dict[str, Dict[str, str]]]:
    """Aplica hashing, enmascarado y tokenización usando solo anonimizar-datos."""

    df_hash = anonimizar_columnas_hash(df, HASH_COLUMNS, sal=HASH_SALT)
    df_enmascarado = enmascarar_columnas(df_hash, MASK_COLUMNS, visible=3, caracter="#")
    tokenizacion = tokenizar_columnas(df_enmascarado, TOKEN_COLUMNS, prefijo="anon")
    return tokenizacion.dataframe, tokenizacion.diccionarios


def guardar_diccionarios(diccionarios: Dict[str, Dict[str, str]]) -> Path:
    """Persiste diccionarios de tokenización para auditorías controladas."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / "tokenizacion.json"
    with destino.open("w", encoding="utf-8") as archivo:
        json.dump(diccionarios, archivo, ensure_ascii=False, indent=2)
    return destino


def guardar_dataset(df: pd.DataFrame, nombre: str) -> Path:
    """Guarda una versión CSV auxiliar para demostrar el before/after."""

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    destino = CACHE_DIR / f"{nombre}.csv"
    df.to_csv(destino, index=False)
    return destino


def presentar_resumen(titulo: str, df: pd.DataFrame, columnas: Iterable[str]) -> None:
    print(f"\n{titulo}")
    print(df[list(columnas)].head())


def ejecutar_pipeline(n_registros: int = DEFAULT_REGISTROS) -> None:
    print("1) Generando datos ficticios con Faker...")
    df_original = generar_datos_ficticios(n_registros=n_registros)
    presentar_resumen(
        "Vista sensible",
        df_original,
        ["cliente_id", "documento_nacional", "direccion_detallada"],
    )
    guardar_dataset(df_original, "dataset_original")

    print("\n2) Enriqueciendo features temporales...")
    df_enriquecido = enriquecer_dataset(df_original)
    presentar_resumen(
        "Features derivadas",
        df_enriquecido,
        ["venta_id", "mes", "es_fin_de_semana"],
    )

    print("\n3) Aplicando hashing, enmascarado y tokenización...")
    df_anonimo, diccionarios = aplicar_anonimizacion(df_enriquecido)
    presentar_resumen(
        "Vista anonimizada",
        df_anonimo,
        ["cliente_id", "documento_nacional", "direccion_detallada", "asesor_venta"],
    )

    ruta_diccionarios = guardar_diccionarios(diccionarios)
    ruta_dataset = guardar_dataset(df_anonimo, "dataset_anonimo")

    print(f"\nDiccionarios guardados en: {ruta_diccionarios}")
    print(f"Dataset anonimizado guardado en: {ruta_dataset}")
    print("Pipeline completado sin exponer los datos originales.")


if __name__ == "__main__":
    ejecutar_pipeline()
