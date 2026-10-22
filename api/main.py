
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "intrusion_detection_pipeline.joblib"

# Load the trained model
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. "
        "Train and save the model before starting the API."
    )

model = joblib.load(MODEL_PATH)

# Create the FastAPI application
app = FastAPI(
    title="AI-Powered Network Intrusion Detection API",
    description=(
        "Predicts whether network traffic is normal or malicious "
        "using a trained machine learning model."
    ),
    version="1.0.0",
)


class TrafficInput(BaseModel):
    features: dict[str, float | int | str] = Field(
        ...,
        description=(
            "Network traffic features using the original UNSW-NB15 "
            "column names, excluding id, label, and attack_cat."
        ),
    )


@app.get("/")
def home():
    return {
        "message": "AI-Powered Network Intrusion Detection API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
    }


@app.post("/predict")
def predict_traffic(payload: TrafficInput):
    try:
        input_df = pd.DataFrame([payload.features])

        # Ensure the input matches the features used during training.
        expected_features = list(
            model.named_steps["preprocessor"].feature_names_in_
        )

        missing = [
            feature for feature in expected_features
            if feature not in input_df.columns
        ]
        extra = [
            feature for feature in input_df.columns
            if feature not in expected_features
        ]

        if missing or extra:
            raise HTTPException(
                status_code=422,
                detail={
                    "message": "Input features do not match the model schema.",
                    "missing_features": missing,
                    "unexpected_features": extra,
                },
            )

        input_df = input_df[expected_features]

        prediction = int(model.predict(input_df)[0])
        probabilities = model.predict_proba(input_df)[0]

        attack_probability = float(probabilities[1])
        normal_probability = float(probabilities[0])

        return {
            "prediction": "Attack" if prediction == 1 else "Normal",
            "label": prediction,
            "attack_probability": round(attack_probability, 4),
            "normal_probability": round(normal_probability, 4),
            "confidence": round(
                max(attack_probability, normal_probability), 4
            ),
            "note": (
                "Model prediction only; not a definitive security verdict."
            ),
        }

    except HTTPException:
        raise
    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=422,
            detail=f"Invalid feature values: {exc}",
        ) from exc
