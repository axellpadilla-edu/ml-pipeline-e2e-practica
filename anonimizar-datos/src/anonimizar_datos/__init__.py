"""Utilidades simples para anonimizar DataFrames de pandas."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from typing import Any, Dict, Iterable, List

import pandas as pd


def _es_na(valor: Any) -> bool:
    try:
        return bool(pd.isna(valor))
    except TypeError:
        return False


def hash_string(valor: Any, *, sal: str | None = None) -> Any:
    """Convierte cualquier valor en un hash SHA-256 determinista."""

    if _es_na(valor):
        return valor  # type: ignore[return-value]

    texto = str(valor)
    payload = f"{sal}:{texto}" if sal else texto
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _asegurar_columnas(columnas: str | Iterable[str]) -> List[str]:
    return [columnas] if isinstance(columnas, str) else list(columnas)


def anonimizar_columnas_hash(
    df: pd.DataFrame,
    columnas: str | Iterable[str],
    *,
    sal: str | None = None,
    inplace: bool = False,
) -> pd.DataFrame:
    """Anonimiza columnas específicas usando hashing determinista."""

    columnas_normalizadas = _asegurar_columnas(columnas)
    destino = df if inplace else df.copy()

    for columna in columnas_normalizadas:
        if columna not in destino.columns:
            raise KeyError(f"La columna '{columna}' no está presente en el DataFrame.")

        destino[columna] = destino[columna].map(lambda v: hash_string(v, sal=sal))

    return destino


def enmascarar_columnas(
    df: pd.DataFrame,
    columnas: str | Iterable[str],
    *,
    visible: int = 4,
    caracter: str = "*",
    inplace: bool = False,
) -> pd.DataFrame:
    """Enmascara parcialmente los valores dejando visibles los últimos caracteres."""

    if visible < 0:
        raise ValueError("El parámetro 'visible' debe ser mayor o igual a cero.")
    if len(caracter) != 1:
        raise ValueError("'caracter' debe contener exactamente un símbolo.")

    columnas_normalizadas = _asegurar_columnas(columnas)
    destino = df if inplace else df.copy()

    for columna in columnas_normalizadas:
        if columna not in destino.columns:
            raise KeyError(f"La columna '{columna}' no está presente en el DataFrame.")

        def _enmascarar(valor: Any) -> Any:
            if _es_na(valor):
                return valor

            texto = str(valor)
            if not texto:
                return texto

            if visible == 0:
                return caracter * len(texto)

            visibles = texto[-visible:]
            relleno = caracter * max(len(texto) - visible, 0)
            return f"{relleno}{visibles}"

        destino[columna] = destino[columna].map(_enmascarar)

    return destino


@dataclass(frozen=True)
class TokenizacionResultado:
    dataframe: pd.DataFrame
    diccionarios: Dict[str, Dict[str, str]]


def tokenizar_columnas(
    df: pd.DataFrame,
    columnas: str | Iterable[str],
    *,
    prefijo: str = "token",
) -> TokenizacionResultado:
    """Reemplaza valores por tokens legibles y conserva el diccionario para auditoría."""

    columnas_normalizadas = _asegurar_columnas(columnas)
    destino = df.copy()
    diccionarios: Dict[str, Dict[str, str]] = {}

    for columna in columnas_normalizadas:
        if columna not in destino.columns:
            raise KeyError(f"La columna '{columna}' no está presente en el DataFrame.")

        mapping: Dict[str, str] = {}
        contador = 1

        def _tokenizar(valor: Any) -> Any:
            nonlocal contador
            if _es_na(valor):
                return valor

            valor_str = str(valor)
            if valor_str not in mapping:
                mapping[valor_str] = f"{prefijo}_{contador:03d}"
                contador += 1
            return mapping[valor_str]

        destino[columna] = destino[columna].map(_tokenizar)
        diccionarios[columna] = mapping

    return TokenizacionResultado(dataframe=destino, diccionarios=diccionarios)


def main() -> None:
    print("anonimizar-datos está listo para anonimizar columnas sensibles.")


__all__ = [
    "TokenizacionResultado",
    "anonimizar_columnas_hash",
    "enmascarar_columnas",
    "hash_string",
    "tokenizar_columnas",
]
