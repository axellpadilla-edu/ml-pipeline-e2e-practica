"""Funciones reutilizables para preparar datos sin fuga de información."""

from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = (
    Path(__file__).resolve().parent.parent.parent / "data" / "bike_sharing_demand.csv"
)
FEATURES = ["temp", "humidity", "windspeed", "hour", "is_weekend"]
TARGET = "demand"


def _validar_dataset() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el dataset en {DATA_PATH}. Ejecuta `uv sync` si faltan dependencias "
            "y valida que los datos estén disponibles."
        )


def cargar_dataframe_limpio() -> pd.DataFrame:
    """Carga el CSV y aplica las transformaciones seguras compartidas."""

    _validar_dataset()
    df = pd.read_csv(DATA_PATH, parse_dates=["timestamp"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], dayfirst=True, errors="coerce")
    df["hour"] = df["timestamp"].dt.hour
    df["is_weekend"] = df["timestamp"].dt.dayofweek >= 5

    columnas_criticas = ["temp", "humidity", "windspeed", TARGET]
    df = df.dropna(subset=columnas_criticas)
    df = df.dropna(subset=["timestamp"])

    return df


def preparar_matrices(
    df: pd.DataFrame,
    target_col: str = TARGET,
    *,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[np.ndarray, np.ndarray, pd.Series, pd.Series]:
    """Genera splits y aplica escalado solo con datos de entrenamiento."""

    X = df[FEATURES]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test


__all__ = [
    "FEATURES",
    "TARGET",
    "cargar_dataframe_limpio",
    "preparar_matrices",
]
