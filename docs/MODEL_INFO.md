# Machine Learning Model Specifications: `loan_model.pkl`

## 1. Overview
This document contains the structural, statistical, and operational analysis of the trained Support Vector Machine (SVM) model (`loan_model.pkl`) used in the Loan Prediction Web Application.

---

## 2. Model Properties

| Parameter | Specification |
| :--- | :--- |
| **Model Type** | `sklearn.svm._classes.SVC` |
| **Kernel Type** | `linear` |
| **Regularization Parameter ($C$)** | `1.0` |
| **Test Accuracy** | ~83.33% |
| **Number of Input Features** | `11` |
| **Expected Input Shape** | `(n_samples, 11)` |
| **Output Classes** | `[0, 1]` (`0`: Loan Not Approved, `1`: Loan Approved) |
| **`predict_proba()` Support** | **False** (`probability=False` on estimator) |
| **Decision Function** | Supported via `decision_function()` |

---

## 3. Input Features & Encoding Rules

The model expects exactly **11 features** in the precise order specified below:

| Index | Feature Name | Data Type | Encoding / Value Range | Description |
| :---: | :--- | :---: | :--- | :--- |
| `0` | `Gender` | `float64` / `int` | `0` = Female, `1` = Male | Applicant's gender |
| `1` | `Married` | `float64` / `int` | `0` = No (Unmarried), `1` = Yes (Married) | Marital status |
| `2` | `Dependents` | `float64` / `int` | `0` = 0, `1` = 1, `2` = 2, `4` = 3+ | Number of dependents |
| `3` | `Education` | `float64` / `int` | `0` = Not Graduate, `1` = Graduate | Educational qualification |
| `4` | `Self_Employed` | `float64` / `int` | `0` = No, `1` = Yes | Self-employment status |
| `5` | `ApplicantIncome` | `float64` | Continuous ($\ge 0$) | Applicant's primary income |
| `6` | `CoapplicantIncome` | `float64` | Continuous ($\ge 0$) | Co-applicant's income |
| `7` | `LoanAmount` | `float64` | Continuous ($\ge 0$) | Loan amount requested (in thousands) |
| `8` | `Loan_Amount_Term` | `float64` | Categorical / Continuous (e.g. 36, 60, 120, 180, 240, 300, 360, 480) | Loan term duration in months |
| `9` | `Credit_History` | `float64` | `0.0` = Bad / No History, `1.0` = Good History | Credit rating guidelines met |
| `10` | `Property_Area` | `float64` / `int` | `0` = Rural, `1` = Semiurban, `2` = Urban | Location area of property |

---

## 4. Preprocessing & Scaling Requirements

1. **No External Scaler Required**: Support vector inspection confirms the model was trained directly on raw continuous features (`ApplicantIncome`, `CoapplicantIncome`, `LoanAmount`, `Loan_Amount_Term`) without standalone MinMax or Standard scaling.
2. **Categorical Encoding**: Web form inputs must be mapped to numeric values using the table above before passing to `model.predict()`.
3. **Data Completeness**: Missing values are not permitted; input validation must ensure all 11 fields are provided.

---

## 5. Model Coefficients Analysis

Linear SVM decision rule formula:
$$z = \mathbf{X} \cdot \mathbf{w}^T + b$$

Where intercept $b = -2.40998829$ and feature weights ($\mathbf{w}$):

- **Credit History (+18.11)**: Dominant positive predictor for loan approval.
- **Education (+2.15)**: Graduate status strongly boosts approval chance.
- **Dependents (+0.68)**: Moderate influence.
- **Property Area (+0.06)**: Slight positive weighting.
- **Applicant Income (+0.00037)**: Positive linear scalar.
- **Self Employed (-1.11)**: Self-employed applicants face higher scrutiny.
- **Married (-0.72)** & **Gender (-0.14)**: Minor negative linear offsets.
- **Loan Term (-0.0247)** & **Coapplicant Income (-0.00013)**: Minor offsets.

---

## 6. Execution Dependencies
- Python 3.10+
- `scikit-learn >= 1.4`
- `numpy >= 1.24`
