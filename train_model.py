
"""Train and save the UNSW-NB15 intrusion detection pipeline."""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


ROOT_DIR = Path(__file__).resolve().parent
DATA_PATH = ROOT_DIR / "data" / "processed" / "UNSW_NB15_training-set.csv"
MODEL_DIR = ROOT_DIR / "models"
MODEL_PATH = MODEL_DIR / "intrusion_detection_pipeline.joblib"

TARGET = "label"
EXCLUDED_COLUMNS = ["id", "label", "attack_cat"]
CATEGORICAL_COLUMNS = ["proto", "service", "state"]


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Training dataset not found: {DATA_PATH}\n"
            "Obtain the UNSW-NB15 training dataset and place it in "
            "data/processed/UNSW_NB15_training-set.csv."
        )

    print("Loading training dataset...")
    data = pd.read_csv(DATA_PATH)

    if TARGET not in data.columns:
        raise ValueError(f"Dataset must contain the '{TARGET}' column.")

    X = data.drop(columns=EXCLUDED_COLUMNS, errors="ignore")
    y = data[TARGET].astype(int)

    categorical = [
        column for column in CATEGORICAL_COLUMNS if column in X.columns
    ]
    numeric = [column for column in X.columns if column not in categorical]

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("numeric", numeric_pipeline, numeric),
            ("categorical", categorical_pipeline, categorical),
        ]
    )

    model = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=100,
                    class_weight="balanced",
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    print(f"Training on {len(data):,} records...")
    model.fit(X, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print("Training completed successfully.")
    print(f"Model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()
