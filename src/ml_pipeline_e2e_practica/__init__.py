"""Paquete educativo con utilidades para prevenir data leakage en pipelines."""

from .preprocesamiento_seguro import (
    FEATURES,
    TARGET,
    cargar_dataframe_limpio,
    preparar_matrices,
)

__all__ = ["FEATURES", "TARGET", "cargar_dataframe_limpio", "preparar_matrices"]
