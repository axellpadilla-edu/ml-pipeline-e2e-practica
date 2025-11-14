"""Entrena y evalúa modelos de clasificación con el pipeline seguro."""

from __future__ import annotations

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

from ml_pipeline_e2e_practica.preprocesamiento_seguro import cargar_dataframe_limpio, preparar_matrices


def comparar_modelos_clasificacion() -> None:
    df = cargar_dataframe_limpio()
    mediana = df["demand"].median()
    df["is_high_demand"] = (df["demand"] > mediana).astype(int)

    X_train, X_test, y_train, y_test = preparar_matrices(df, target_col="is_high_demand")

    modelos = {
        "LogisticRegression": LogisticRegression(max_iter=1000),
        "KNeighborsClassifier": KNeighborsClassifier(n_neighbors=5),
    }

    print("Comparativa de modelos de clasificación (Accuracy en set de prueba):")
    for nombre, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        predicciones = modelo.predict(X_test)
        accuracy = accuracy_score(y_test, predicciones)
        print(f"- {nombre}: {accuracy:.4f}")


if __name__ == "__main__":
    comparar_modelos_clasificacion()
