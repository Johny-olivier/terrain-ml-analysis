from __future__ import annotations

import pandas as pd
from sklearn.linear_model import LinearRegression


DATASET_PATH = "terrain_1M.csv"
TARGET_COLUMN = "prix_m2"

NUMERIC_FEATURES = [
    "acces_voiture",
    "distance_rn",
    "batissable",
    "distance_jirama",
]

CATEGORICAL_FEATURES = ["commune", "type_papier"]

REQUIRED_COLUMNS = {
    "commune",
    "prix_total",
    "surface",
    "acces_voiture",
    "distance_rn",
    "batissable",
    "distance_jirama",
    "type_papier",
}

# Coordonnees approximatives pour l'affichage cartographique.
COMMUNE_COORDS = {
    "Ivato": (-18.7969, 47.4776),
    "Itaosy": (-18.9533, 47.4883),
    "Alasora": (-18.9667, 47.5667),
    "Talatamaty": (-18.8333, 47.4500),
    "Ambohidratrimo": (-18.8167, 47.4167),
    "Analamahitsy": (-18.8800, 47.5400),
    "Ivandry": (-18.8650, 47.5300),
    "Ambatobe": (-18.8500, 47.5600),
    "Ambohimangakely": (-18.9160, 47.6150),
    "Ankadikely": (-18.8820, 47.6140),
    "Sabotsy Namehana": (-18.8720, 47.5830),
    "Ambohimalaza": (-18.9260, 47.6400),
    "Andoharanofotsy": (-18.9980, 47.5300),
    "Ambohijanaka": (-19.0330, 47.5460),
    "Manakambahiny": (-18.9100, 47.5450),
}


def load_dataset(path: str = DATASET_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)

    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        missing_list = ", ".join(sorted(missing_columns))
        raise ValueError(f"Colonnes manquantes dans {path}: {missing_list}")

    df = df.copy()
    df[TARGET_COLUMN] = df["prix_total"] / df["surface"]
    return df


def encode_features(df: pd.DataFrame) -> pd.DataFrame:
    feature_columns = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = df[feature_columns].copy()
    return pd.get_dummies(X, columns=CATEGORICAL_FEATURES, drop_first=True)


def train_linear_regression(df: pd.DataFrame) -> tuple[LinearRegression, list[str]]:
    X = encode_features(df)
    y = df[TARGET_COLUMN]

    model = LinearRegression()
    model.fit(X, y)

    return model, X.columns.tolist()


def build_prediction_frame(
    columns: list[str],
    *,
    acces_voiture: int,
    distance_rn: int,
    batissable: int,
    distance_jirama: int,
    commune: str,
    type_papier: str,
) -> pd.DataFrame:
    data = {
        "acces_voiture": acces_voiture,
        "distance_rn": distance_rn,
        "batissable": batissable,
        "distance_jirama": distance_jirama,
    }

    commune_col = f"commune_{commune}"
    type_col = f"type_papier_{type_papier}"

    if commune_col in columns:
        data[commune_col] = 1

    if type_col in columns:
        data[type_col] = 1

    return pd.DataFrame([{column: data.get(column, 0) for column in columns}])
