# AI-Powered Network Intrusion Detection System

An AI-powered cybersecurity project that applies machine learning to network traffic classification to identify potentially malicious activity. The system uses the UNSW-NB15 dataset, a Scikit-learn Random Forest pipeline, a FastAPI prediction service, and a Streamlit dashboard.

## Project Overview

Network intrusion detection is an important component of cybersecurity. Traditional detection approaches can struggle to identify complex traffic patterns and previously unseen combinations of network behaviors.

This project explores supervised machine learning for binary network traffic classification, distinguishing between **Normal** traffic and **Attack** traffic. It provides a reusable model pipeline, a REST API for predictions, and an interactive dashboard for testing and evaluating the model.

**Important:** This is a research and educational prototype. Its predictions are not a definitive security verdict and should not be used as the sole basis for security decisions.

## Key Features

- **Machine learning:** Random Forest classification using Scikit-learn.
- **Data preprocessing:** A pipeline for preprocessing numerical and categorical features.
- **Binary classification:** Predicts whether supplied network traffic is Normal or Attack.
- **REST API:** FastAPI endpoints for health checks and model predictions.
- **Interactive dashboard:** Streamlit interface for entering traffic features and viewing predictions.
- **Model evaluation:** Accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix.
- **Model comparison:** Results from evaluating multiple machine learning algorithms.
- **Reproducibility:** A training script and dependency list for setting up the project.

## Technology Stack

| Component | Technologies |
|---|---|
| Programming language | Python |
| Data analysis | Pandas, NumPy |
| Machine learning | Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Model persistence | Joblib |
| API development | FastAPI, Uvicorn |
| Dashboard | Streamlit |
| Dataset | UNSW-NB15 |
| Development tools | VS Code, Jupyter Notebook, Git, GitHub |

## Dataset

This project uses the **UNSW-NB15 dataset**, a network intrusion detection dataset developed for cybersecurity research.

Official dataset source:  
https://research.unsw.edu.au/projects/unsw-nb15-dataset

The dataset contains normal network traffic and multiple categories of malicious activity. The project uses a binary classification target:

- `0` — Normal traffic
- `1` — Attack traffic

The model uses 42 input features after excluding the record identifier and target-related columns: `id`, `label`, and `attack_cat`.

Categorical features include `proto`, `service`, and `state`. These features are handled by the preprocessing pipeline.

### Dataset preparation

The original dataset files and processed training and testing files are not included in the GitHub repository because of their size and the project's `.gitignore` rules.

After cloning the repository:

1. Download the UNSW-NB15 dataset from the official source.
2. Prepare the training and testing datasets in the format expected by `train_model.py`.
3. Create the `data/processed/` directory if it does not exist.
4. Place the processed files there using these exact filenames:

```text
data/processed/
├── UNSW_NB15_training-set.csv
└── UNSW_NB15_testing-set.csv
```

The training and testing files should retain the expected feature columns and target labels.

## Project Structure

```text
AI-Powered-Network-Intrusion-Detection-System/
├── api/
│   └── main.py
├── dashboard/
│   └── app.py
├── data/
│   └── processed/
│       ├── UNSW_NB15_training-set.csv
│       └── UNSW_NB15_testing-set.csv
├── models/
│   └── intrusion_detection_pipeline.joblib
├── notebooks/
│   └── 01_data_exploration.ipynb
├── results/
│   ├── figures/
│   │   └── model_performance_comparison.png
│   ├── final_evaluation_report.txt
│   └── model_comparison.csv
├── src/
├── train_model.py
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** The dataset files and trained model shown in this tree are local runtime artifacts and are excluded from GitHub. The original downloaded dataset files may also be stored under `data/` during local development. The `src/` directory is reserved for supporting source modules.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Zolla21/AI-Powered-Network-Intrusion-Detection-System.git
cd AI-Powered-Network-Intrusion-Detection-System
```

### 2. Create and activate a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, consult the official Python or Microsoft documentation for virtual environment activation policies.

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Prepare the dataset and train the model

Ensure the processed training and testing CSV files are in `data/processed/`, using the filenames specified in the Dataset section.

Run:

```powershell
python train_model.py
```

The training script trains the machine learning pipeline and saves the resulting model to:

```text
models/intrusion_detection_pipeline.joblib
```

Training time depends on the computer, dataset, and model configuration.

## Running the REST API

Start the FastAPI application from the project root with the virtual environment activated:

```powershell
python -m uvicorn api.main:app --reload
```

The local API address is:

http://127.0.0.1:8000

### API documentation

Open the interactive Swagger documentation:

http://127.0.0.1:8000/docs

### Available endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Checks API health and whether the model is loaded |
| POST | `/predict` | Predicts a traffic class from the supplied features |

The health endpoint should report that the service is healthy and the model is loaded when startup is successful.

Use the Swagger interface to inspect the required request format and test predictions against the API.

## Running the Streamlit Dashboard

Open a separate PowerShell terminal, activate the same virtual environment, and navigate to the project root.

Run:

```powershell
python -m streamlit run dashboard/app.py
```

Open the dashboard at:

http://localhost:8501

The dashboard provides an interactive interface for entering network traffic features, generating a model prediction, and viewing model evaluation information.

Run the API and dashboard in separate terminals when using both simultaneously.

## Model Training and Evaluation

The project includes a Random Forest pipeline and evaluation results from experiments comparing multiple machine learning algorithms.

The evaluated algorithms include:

- Logistic Regression
- Decision Tree
- Random Forest
- Support Vector Machine (SVM)
- Gradient Boosting

The evaluation uses standard binary classification metrics:

| Metric | Purpose |
|---|---|
| Accuracy | Proportion of correctly classified observations |
| Precision | Proportion of predicted attacks that are actual attacks |
| Recall | Proportion of actual attacks identified by the model |
| F1-score | Harmonic mean of precision and recall |
| ROC-AUC | Ability to distinguish between the two classes across classification thresholds |
| Confusion matrix | Breakdown of correct and incorrect predictions |

### Reported model performance

The current Random Forest pipeline evaluation reported the following results:

| Metric | Score |
|---|---:|
| Accuracy | 0.892 |
| Precision | 0.851 |
| Recall | 0.975 |
| F1-score | 0.909 |
| ROC-AUC | 0.980 |

These are the project's reported evaluation results, not a guarantee of performance on live network traffic. Consult `results/final_evaluation_report.txt` and `results/model_comparison.csv` for the saved experiment results.

### Evaluation outputs

The project stores its evaluation artifacts in the `results/` directory:

- `final_evaluation_report.txt` — text-based evaluation report.
- `model_comparison.csv` — comparative model results.
- `figures/model_performance_comparison.png` — model performance comparison visualization.

## Security Considerations and Limitations

- The model learns patterns from the dataset used during training and may not generalize to all real-world network environments.
- Predictions can include false positives and false negatives.
- High recall does not mean every attack will be detected.
- Dataset imbalance, data leakage, preprocessing errors, and differences between training and deployment traffic can affect results.
- The API accepts model input for classification; it does not independently capture or monitor live network packets.
- The application is a prototype and does not replace a production intrusion detection or prevention system.
- Before production use, implement appropriate authentication, authorization, input validation, logging, monitoring, secure deployment, and independent security testing.
- Only use network data that you are authorized to collect and analyze.

## Future Improvements

Potential extensions include:

- Integrating live network traffic capture.
- Adding multiclass attack classification.
- Evaluating additional machine learning and deep learning models.
- Improving detection of previously unseen attacks.
- Adding explainable AI techniques to interpret predictions.
- Developing automated monitoring and alerting.
- Deploying the API and dashboard to a secure cloud environment.
- Adding automated testing and a continuous integration workflow.

## Author

**Zelalem Fissiha**

Fullstack Developer | Data Analyst | Machine Learning Researcher | Lecturer

GitHub: https://github.com/Zolla21

Portfolio: https://zolla21.github.io/

## License

No license is specified in this repository unless a license file is added. All rights to the project remain with their respective owners, subject to the applicable dataset terms and any third-party licenses.

