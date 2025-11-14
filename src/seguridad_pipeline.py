"""Pipeline seguro para el dataset de demanda de bicicletas."""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = Path(__file__).parent.parent / "data" / "bike_sharing_demand.csv"


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"No se encontró el dataset en {DATA_PATH}. Asegúrate de sincronizar los datos."
        )

    df = pd.read_csv(DATA_PATH, parse_dates=["datetime"])
    df["hour"] = df["datetime"].dt.hour
    df["is_weekend"] = df["datetime"].dt.dayofweek >= 5

    features = ["temp", "humidity", "windspeed", "hour", "is_weekend"]
    target = "count"

    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()

    # Regla de Oro: se ajusta (fit) el scaler solo con el set de entrenamiento para evitar leakage.
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Resumen del pipeline seguro:")
    print(f"- Registros totales: {len(df):,}")
    print(f"- Train shape: {X_train.shape}")
    print(f"- Test shape: {X_test.shape}")
    print(f"- Media entrenamiento (primer feature): {X_train_scaled[:, 0].mean():.3f}")
    print(f"- Media prueba (primer feature): {X_test_scaled[:, 0].mean():.3f}")
    print("El scaler solo " "vio" " el set de entrenamiento, evitando fugas de información.")


if __name__ == "__main__":
    main()
