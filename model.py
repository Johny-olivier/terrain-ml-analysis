import joblib

from ml_utils import DATASET_PATH, load_dataset, train_linear_regression


def main() -> None:
    df = load_dataset(DATASET_PATH)
    model, columns = train_linear_regression(df)

    joblib.dump((model, columns), "model.pkl")

    print("Modele sauvegarde dans model.pkl")
    print(f"Lignes d'apprentissage : {len(df):,}")
    print(f"Nombre de variables apres encodage : {len(columns)}")


if __name__ == "__main__":
    main()
