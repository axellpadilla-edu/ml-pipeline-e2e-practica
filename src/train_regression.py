"""Entrena y evalúa modelos de regresión con el pipeline seguro."""

from __future__ import annotations

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor

from ml_pipeline_e2e_practica.preprocesamiento_seguro import cargar_dataframe_limpio, preparar_matrices


def comparar_modelos_regresion() -> None:
    df = cargar_dataframe_limpio()
    X_train, X_test, y_train, y_test = preparar_matrices(df)

    modelos = {
        "LinearRegression": LinearRegression(),
        "DecisionTreeRegressor": DecisionTreeRegressor(random_state=42),
    }

    print("Comparativa de modelos de regresión (MSE en set de prueba):")
    for nombre, modelo in modelos.items():
        modelo.fit(X_train, y_train)
        predicciones = modelo.predict(X_test)
        mse = mean_squared_error(y_test, predicciones)
        print(f"- {nombre}: {mse:.4f}")


if __name__ == "__main__":
    comparar_modelos_regresion()
