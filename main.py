import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

from ml_utils import DATASET_PATH, TARGET_COLUMN, encode_features, load_dataset


def main() -> None:
    df = load_dataset(DATASET_PATH)

    print("Apercu du dataset :")
    print(df.head())
    print()

    X = encode_features(df)
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    pred = model.predict(X_test)

    print(f"Taille du dataset : {len(df):,}")
    print(f"Variables utilisees : {len(X.columns)}")
    print(f"MAE : {mean_absolute_error(y_test, pred):,.2f} Ar/m2")
    print(f"R2 : {r2_score(y_test, pred):.4f}")

    coef_series = pd.Series(model.coef_, index=X.columns)
    coef_series = coef_series.sort_values(key=lambda values: values.abs(), ascending=False)

    print("\nTop 10 coefficients en valeur absolue :")
    for name, coef in coef_series.head(10).items():
        print(f"{name}: {coef:,.2f}")

    test = X_test.iloc[[0]]
    print(f"\nPrediction test : {model.predict(test)[0]:,.2f} Ar/m2")
    print(f"Valeur reelle   : {y_test.iloc[0]:,.2f} Ar/m2")


if __name__ == "__main__":
    main()
