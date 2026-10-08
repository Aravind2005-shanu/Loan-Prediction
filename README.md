# Loan Prediction Machine Learning Web Application

A production-style machine learning web application that predicts loan approval eligibility based on applicant demographics, financial profile, credit history, and loan request parameters. Built with **Python, FastAPI, Scikit-learn, HTML5, CSS3, and Vanilla JavaScript**.

---

## 1. Overview
This web application transforms a pre-trained **Support Vector Machine (SVM)** classifier into a production-style application. The backend is served by **FastAPI**, providing input validation, REST API endpoints, and direct integration with the trained binary classifier `loan_model.pkl`. The frontend is built using standard **HTML5, CSS3, and Vanilla JavaScript** without any JavaScript frameworks or build tools.

---

## 2. Problem Statement
Financial institutions evaluate loan applications based on risk factors such as income level, credit history, loan amount, education, and employment status. Manual verification is time-consuming and prone to human error. An automated machine learning model can instantly evaluate applicant eligibility based on historical approval patterns.

---

## 3. Project Objective
To create a clean, responsive, end-to-end loan evaluation web application that takes user input from a custom web interface, formats and encodes the feature vector according to the exact training protocol, performs real-time inference using `loan_model.pkl`, and presents clear visual feedback to the user.

---

## 4. Features
- **Real ML Predictions**: Uses the trained `loan_model.pkl` SVM binary classifier (no fake rules).
- **FastAPI Backend**: Provides asynchronous API handling, strict Pydantic schema validation, and health monitoring.
- **Pure Web Frontend**: Built strictly with HTML5, CSS3, and Vanilla JavaScript (No React, Vite, or Node.js required).
- **FinTech UI Design**: Modern dark theme with sectioned form cards, responsive grid, and custom typography.
- **Client & Server Input Validation**: Dual-layer input checking with inline error displays.
- **Loading & State Handling**: Displays animated loading indicators while disabling submission buttons to prevent duplicate requests.
- **Comprehensive Test Suite**: Automated pytest test suite covering prediction logic and REST endpoints.
- **Zero Raw Stack Traces**: Custom global exception handlers hide internal tracebacks from end users.

---

## 5. Machine Learning Model
- **Algorithm**: Support Vector Machine (`sklearn.svm.SVC`)
- **Kernel**: Linear (`kernel='linear'`, `C=1.0`)
- **Input Features**: 11 features
- **Output Labels**: `0` (Loan Not Approved) / `1` (Loan Approved)
- **`predict_proba()`**: Not available (`probability=False`)

---

## 6. Dataset
The model was trained on the standard Loan Eligibility Dataset (Analytics Vidhya / Kaggle format), containing 614 records with categorical applicant demographics and continuous financial metrics.

---

## 7. Data Preprocessing
Categorical features are encoded to numeric representations matching training:
- **Gender**: `0` = Female, `1` = Male
- **Married**: `0` = No, `1` = Yes
- **Dependents**: `0` = 0, `1` = 1, `2` = 2, `4` = 3+
- **Education**: `0` = Not Graduate, `1` = Graduate
- **Self_Employed**: `0` = No, `1` = Yes
- **Credit_History**: `0.0` = Bad / No History, `1.0` = Meets Guidelines
- **Property_Area**: `0` = Rural, `1` = Semiurban, `2` = Urban

---

## 8. Model Training
The model was trained in Google Colab using scikit-learn's `SVC` classifier with a linear kernel, capturing non-linear feature interactions through support vector optimization.

---

## 9. Model Evaluation
- **Test Accuracy**: Approximately **83.33%**
- **Primary Driver**: Credit history guidelines met ($w_{CreditHistory} \approx +18.11$) followed by graduate education status ($w_{Education} \approx +2.15$).

---

## 10. Technology Stack
- **Backend**: Python 3.10+, FastAPI, Uvicorn, Pydantic
- **Machine Learning**: Scikit-learn, NumPy, Pandas
- **Frontend**: HTML5, CSS3 (Custom CSS Grid & Flexbox), Vanilla JavaScript (Fetch API)
- **Testing**: Pytest, HTTPX

---

## 11. System Architecture

```text
Browser User Interface (HTML5/CSS3/Vanilla JS)
             │
             │ HTTP POST /predict (JSON Payload)
             ▼
      FastAPI Web Server (backend/app.py)
             │
             │ Pydantic Validation & Encoding (backend/validation.py)
             ▼
   ML Prediction Engine (backend/prediction.py)
             │
             │ DataFrame (1x11 Feature Matrix)
             ▼
     SVM Classifier Model (loan_model.pkl)
             │
             │ Prediction Output [0 or 1]
             ▼
      JSON Response -> UI Updates Card Display
```

---

## 12. Project Structure

```text
Loan-Prediction/
│
├── loan_model.pkl
│
├── backend/
│   ├── app.py
│   ├── model_loader.py
│   ├── prediction.py
│   ├── validation.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── app.js
│   └── assets/
│
├── tests/
│   ├── test_prediction.py
│   └── test_api.py
│
├── docs/
│   ├── MODEL_INFO.md
│   └── API_DOCUMENTATION.md
│
├── README.md
├── .gitignore
└── LICENSE
```

---

## 13. API Documentation
See detailed documentation in [`docs/API_DOCUMENTATION.md`](file:///c:/Users/tulas/OneDrive/Desktop/Loan-Prediction/docs/API_DOCUMENTATION.md).

Quick summary of endpoints:
- `GET /` — Serves frontend application.
- `GET /health` — Health check endpoint.
- `POST /predict` — Performs loan eligibility prediction.

---

## 14. Installation

1. Clone or open the project directory:
```bash
cd Loan-Prediction
```

2. Install backend dependencies:
```bash
pip install -r backend/requirements.txt
```

---

## 15. Running the Application

Start the FastAPI application server with Uvicorn:

```bash
uvicorn backend.app:app --reload
```

Open your browser and navigate to:
```text
http://127.0.0.1:8000
```

---

## 16. Testing

Execute the automated pytest suite:

```bash
python -m pytest tests/
```

All unit tests and API integration tests should pass with status 200/422 assertions.

---

## 17. Screenshots
*(Placeholder: Screenshots of Application UI)*
- **Applicant Form View**: Clean multi-column form with modern inputs.
- **Approved State**: Emerald green success card showing `✓ LOAN APPROVED`.
- **Rejected State**: Rose red warning card showing `✕ LOAN NOT APPROVED`.

---

## 18. Future Improvements
- Model retrain pipeline integration.
- SHAP or LIME explainability visualizations for individual predictions.
- PDF summary report download for applicants.

---

## 19. Disclaimer
This application is a machine learning demonstration. The prediction is not a real financial approval decision and should not be used as financial advice.

---

## 20. Author
Senior Machine Learning & Software Engineering Implementation.
