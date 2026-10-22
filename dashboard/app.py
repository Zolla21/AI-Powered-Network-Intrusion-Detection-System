
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# Project configuration
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "intrusion_detection_pipeline.joblib"

st.set_page_config(
    page_title="AI Network Intrusion Detection",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ AI-Powered Network Intrusion Detection")
st.write(
    "Analyze network traffic using a machine learning model "
    "trained on the UNSW-NB15 dataset."
)

if not MODEL_PATH.exists():
    st.error(f"Trained model not found: {MODEL_PATH}")
    st.stop()


@st.cache_resource
def load_model(path):
    return joblib.load(path)


model = load_model(str(MODEL_PATH))
preprocessor = model.named_steps["preprocessor"]
expected_features = list(preprocessor.feature_names_in_)

st.success("Model loaded successfully.")

st.info(
    "Enter the 42 network traffic features below. "
    "The initial values are illustrative and are not a real traffic capture."
)

with st.form("traffic_form"):
    st.subheader("Network Traffic Features")

    feature_values = {}

    numeric_features = [
        name for name in expected_features
        if name not in {"proto", "service", "state"}
    ]

    categorical_features = ["proto", "service", "state"]

    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("**Traffic and connection details**")

        for feature in numeric_features[:21]:
            feature_values[feature] = st.number_input(
                feature,
                value=0.0,
                format="%.6f",
                help=f"Enter the value for {feature}.",
            )

    with right_col:
        st.markdown("**Remaining traffic features**")

        for feature in numeric_features[21:]:
            feature_values[feature] = st.number_input(
                feature,
                value=0.0,
                format="%.6f",
                help=f"Enter the value for {feature}.",
            )

        st.markdown("**Categorical features**")

        feature_values["proto"] = st.text_input(
            "Protocol (proto)", value="tcp"
        )
        feature_values["service"] = st.text_input(
            "Service", value="http"
        )
        feature_values["state"] = st.text_input(
            "Connection state", value="FIN"
        )

    submitted = st.form_submit_button(
        "Analyze Network Traffic",
        type="primary",
        use_container_width=True,
    )

if submitted:
    # Restore the original feature order used during training.
    input_df = pd.DataFrame(
        [{feature: feature_values[feature] for feature in expected_features}]
    )

    prediction = int(model.predict(input_df)[0])
    probabilities = model.predict_proba(input_df)[0]

    normal_probability = float(probabilities[0])
    attack_probability = float(probabilities[1])

    st.subheader("Prediction Results")

    result_col, normal_col, attack_col = st.columns(3)

    with result_col:
        if prediction == 1:
            st.error("Prediction: ATTACK")
        else:
            st.success("Prediction: NORMAL")

    with normal_col:
        st.metric(
            "Normal probability",
            f"{normal_probability:.1%}",
        )

    with attack_col:
        st.metric(
            "Attack probability",
            f"{attack_probability:.1%}",
        )

    st.progress(attack_probability, text="Estimated attack probability")

    st.warning(
        "This is a machine-learning estimate, not a definitive security "
        "verdict. The quality of the prediction depends on valid, "
        "representative input features."
    )

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)

st.header("Model Evaluation")
st.write("Performance on the held-out UNSW-NB15 test dataset.")

# Load the original test dataset
TEST_PATH = BASE_DIR / "data" / "processed" / "UNSW_NB15_testing-set.csv"

if TEST_PATH.exists():
    @st.cache_data
    def load_test_data(path):
        return pd.read_csv(path)

    test_df = load_test_data(str(TEST_PATH))
    y_test = test_df["label"].astype(int)
    X_test = test_df.drop(columns=["id", "label", "attack_cat"])

    # Predict with the saved pipeline
    y_test_pred = model.predict(X_test)
    y_test_prob = model.predict_proba(X_test)[:, 1]

    metric_cols = st.columns(5)

    metrics = [
        ("Accuracy", accuracy_score(y_test, y_test_pred)),
        ("Precision", precision_score(y_test, y_test_pred, zero_division=0)),
        ("Recall", recall_score(y_test, y_test_pred, zero_division=0)),
        ("F1-Score", f1_score(y_test, y_test_pred, zero_division=0)),
        ("ROC-AUC", roc_auc_score(y_test, y_test_prob)),
    ]

    for col, (name, value) in zip(metric_cols, metrics):
        col.metric(name, f"{value:.3f}")

    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, y_test_pred)

    cm_df = pd.DataFrame(
        cm,
        index=["Actual Normal", "Actual Attack"],
        columns=["Predicted Normal", "Predicted Attack"],
    )

    st.dataframe(cm_df, use_container_width=True)

    st.caption(
        "Metrics are calculated from the saved model on the held-out test set. "
        "They may differ from the earlier comparison if model configurations differ."
    )
else:
    st.warning(
        "Test dataset not found. Expected location: "
        f"{TEST_PATH}"
    )

st.write("Performance on the held-out UNSW-NB15 test dataset.")

# Load the original test dataset
TEST_PATH = BASE_DIR / "data" / "processed" / "UNSW_NB15_testing-set.csv"

if TEST_PATH.exists():
    @st.cache_data
    def load_test_data(path):
        return pd.read_csv(path)

    test_df = load_test_data(str(TEST_PATH))
    y_test = test_df["label"].astype(int)
    X_test = test_df.drop(columns=["id", "label", "attack_cat"])

    # Predict with the saved pipeline
    y_test_pred = model.predict(X_test)
    y_test_prob = model.predict_proba(X_test)[:, 1]

    metric_cols = st.columns(5)

    metrics = [
        ("Accuracy", accuracy_score(y_test, y_test_pred)),
        ("Precision", precision_score(y_test, y_test_pred, zero_division=0)),
        ("Recall", recall_score(y_test, y_test_pred, zero_division=0)),
        ("F1-Score", f1_score(y_test, y_test_pred, zero_division=0)),
        ("ROC-AUC", roc_auc_score(y_test, y_test_prob)),
    ]

    for col, (name, value) in zip(metric_cols, metrics):
        col.metric(name, f"{value:.3f}")

    st.subheader("Confusion Matrix")
    cm = confusion_matrix(y_test, y_test_pred)

    cm_df = pd.DataFrame(
        cm,
        index=["Actual Normal", "Actual Attack"],
        columns=["Predicted Normal", "Predicted Attack"],
    )

    st.dataframe(cm_df, use_container_width=True)

    st.caption(
        "Metrics are calculated from the saved model on the held-out test set. "
        "They may differ from the earlier comparison if model configurations differ."
    )
else:
    st.warning(
        "Test dataset not found. Expected location: "
        f"{TEST_PATH}"
    )

st.divider()
st.caption(
    "AI-Powered Network Intrusion Detection | "
    "Python · Streamlit · scikit-learn · UNSW-NB15"
)
