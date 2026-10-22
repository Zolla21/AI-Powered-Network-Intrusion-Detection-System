\# AI-Powered Network Intrusion Detection



An intelligent network intrusion detection system that uses machine learning to classify network traffic as \*\*Normal\*\* or \*\*Attack\*\*. The project uses the UNSW-NB15 dataset and provides a REST API and an interactive Streamlit dashboard.



\## Project Overview



Network intrusion detection helps identify suspicious activity and potential cyberattacks by analyzing network traffic characteristics. This project applies supervised machine learning to classify network traffic and provide estimated probabilities for normal and malicious traffic.



The system is designed as a practical cybersecurity and machine learning portfolio project.



\## Key Features



\- Binary classification of network traffic: Normal or Attack.

\- Data preprocessing for numerical and categorical features.

\- Comparison of multiple machine learning algorithms.

\- Random Forest classification pipeline.

\- Evaluation using accuracy, precision, recall, F1-score, and ROC-AUC.

\- Confusion matrix for evaluating classification errors.

\- FastAPI REST API for network traffic predictions.

\- Interactive Streamlit dashboard.

\- Saved model comparison results and evaluation reports.



\## Technology Stack



| Component | Technologies |

|---|---|

| Programming language | Python |

| Data analysis | Pandas, NumPy |

| Machine learning | scikit-learn |

| Data visualization | Matplotlib, Seaborn |

| Model persistence | Joblib |

| REST API | FastAPI, Uvicorn |

| Web dashboard | Streamlit |

| Development environment | Jupyter Notebook, VS Code |



\## Dataset



This project uses the \*\*UNSW-NB15\*\* network intrusion detection dataset.



Official source: \[UNSW-NB15 Dataset](https://research.unsw.edu.au/projects/unsw-nb15-dataset)



The prepared training and testing datasets contain network traffic features and a binary label:



\- `0`: Normal traffic

\- `1`: Attack traffic



The `attack\_cat` field and record identifier are excluded from the binary classification input features to prevent target leakage.



\*\*Dataset note:\*\* The dataset is not included in this repository. Obtain it from the official source and place the prepared training and testing CSV files in `data/processed/` as described below. Follow the dataset provider's terms and attribution requirements.



\## Project Structure



```text

ai-intrusion-detection/

├── api/

│   └── main.py

├── dashboard/

│   └── app.py

├── data/

│   ├── raw/

│   └── processed/

│       ├── UNSW\_NB15\_training-set.csv

│       └── UNSW\_NB15\_testing-set.csv

├── models/

│   └── intrusion\_detection\_pipeline.joblib

├── notebooks/

│   └── 01\_data\_exploration.ipynb

├── results/

│   ├── figures/

│   │   └── model\_performance\_comparison.png

│   ├── model\_comparison.csv

│   └── final\_evaluation\_report.txt

├── src/

├── .gitignore

├── requirements.txt

└── README.md

```



Generated model files and dataset files may be excluded from Git through `.gitignore`. Their presence in this example describes the local development setup, not necessarily the contents of the published repository.



\## Installation



\### 1. Clone the repository



```bash

git clone https://github.com/Zolla21/AI-Powered-Network-Intrusion-Detection-System.git

cd ai-intrusion-detection

```





\### 2. Create a virtual environment



On Windows PowerShell:



```powershell

python -m venv .venv

.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install dependencies



```powershell

python -m pip install --upgrade pip

pip install -r requirements.txt

```



\### 4. Prepare the dataset and model


### 4. Prepare the Dataset and Train the Model

#### Download the dataset

Obtain the UNSW-NB15 dataset from the official source:

https://research.unsw.edu.au/projects/unsw-nb15-dataset

Prepare the training and testing CSV files and place them in `data/processed/` using these exact filenames:

- `UNSW_NB15_training-set.csv`
- `UNSW_NB15_testing-set.csv`

The dataset is not included in this repository. Follow the dataset provider's terms and attribution requirements.

#### Train the model

From the project root, run:

```powershell
python train_model.py
```

The script trains a Random Forest classification pipeline and saves the trained model to:

```text
models/intrusion_detection_pipeline.joblib
```

The `models/` directory is created automatically if it does not exist.

The generated model is excluded from Git because of its size. Run the training script to recreate it locally before starting the API or dashboard.

#### Explore the data

To explore the dataset, compare models, and review evaluation results, open:

`notebooks/01_data_exploration.ipynb`





## Running the API



Start the FastAPI server from the project root:



```powershell

python -m uvicorn api.main:app --reload

```



API endpoints:



| Method | Endpoint | Purpose |

|---|---|---|

| GET | `/` | API information |

| GET | `/health` | Check API and model status |

| POST | `/predict` | Classify network traffic |



Interactive API documentation:



\[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)



The prediction endpoint accepts a JSON object containing the 42 input features used by the trained model, excluding `id`, `label`, and `attack\_cat`.



\## Running the Dashboard



Start Streamlit in a separate terminal:



```powershell

python -m streamlit run dashboard/app.py

```



Open the dashboard at:



\[http://localhost:8501](http://localhost:8501)



The dashboard supports interactive predictions and displays model evaluation metrics and a confusion matrix.



\## Model Evaluation



The project compares the following algorithms:



\- Logistic Regression

\- Decision Tree

\- Random Forest

\- Histogram-based Gradient Boosting



Evaluation metrics include:



\- \*\*Accuracy:\*\* Overall proportion of correct predictions.

\- \*\*Precision:\*\* Proportion of predicted attacks that are actual attacks.

\- \*\*Recall:\*\* Proportion of actual attacks detected.

\- \*\*F1-score:\*\* Harmonic mean of precision and recall.

\- \*\*ROC-AUC:\*\* Ability to distinguish between normal and attack traffic.



Results are saved in `results/model\_comparison.csv`, with the comparison chart in `results/figures/model\_performance\_comparison.png`.



The final model's evaluation report is saved in `results/final\_evaluation\_report.txt`.



Actual performance figures should be taken from the generated evaluation files rather than assumed from the project description.



\## Security and Limitations



\- Predictions are model estimates and are not definitive security verdicts.

\- The model's performance depends on input quality and how closely real network traffic resembles the training data.

\- The current application accepts manually supplied feature values; it does not capture live packets or automatically monitor a network interface.

\- The project is a prototype and should not be treated as a production security control without additional validation, monitoring, and security testing.

\- Model probabilities may require calibration before they can be interpreted as reliable real-world risk estimates.



\## Future Improvements



\- Integrate live network traffic capture.

\- Add explainable AI for individual predictions.

\- Extend the system to classify specific attack categories.

\- Improve input validation and API security.

\- Add authentication, logging, and monitoring.

\- Deploy the API and dashboard to a cloud environment.

\- Add automated testing and continuous integration.



\## Author



\*\*Zelalem Fissiha\*\*



Fullstack Developer | Data Analyst | Machine Learning Researcher | Lecturer



This project demonstrates practical skills in machine learning, data preprocessing, model evaluation, REST API development, and interactive dashboard design.



\## License



Add an appropriate license before distributing the source code. Verify the dataset's own terms separately.




