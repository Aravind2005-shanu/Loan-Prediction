# API Documentation: Loan Prediction Web Application

This document provides complete technical documentation for the RESTful endpoints exposed by the FastAPI backend server.

---

## Base URL
```text
http://127.0.0.1:8000
```

---

## Endpoints Overview

| Method | Endpoint | Description | Auth Required |
| :---: | :--- | :--- | :---: |
| `GET` | `/` | Serves the single-page HTML application | No |
| `GET` | `/health` | Application & ML model health check | No |
| `POST` | `/predict` | Evaluates loan application with trained SVM model | No |

---

## 1. `GET /`

### Purpose
Serves the responsive single-page web interface (`index.html`) to the user browser.

### Request Format
- Headers: Standard HTTP GET headers

### Response Format
- Status Code: `200 OK`
- Content-Type: `text/html; charset=utf-8`

---

## 2. `GET /health`

### Purpose
Returns system and model availability status for monitoring and uptime checks.

### Request Format
```http
GET /health HTTP/1.1
Host: 127.0.0.1:8000
```

### Response Format (Healthy)
- Status Code: `200 OK`
- Content-Type: `application/json`

```json
{
  "status": "healthy"
}
```

### Response Format (Service Unavailable)
- Status Code: `503 Service Unavailable`
- Content-Type: `application/json`

```json
{
  "status": "unhealthy",
  "detail": "Model is not loaded"
}
```

---

## 3. `POST /predict`

### Purpose
Receives applicant information, performs input validation and categorical encoding, and passes the 11-dimensional feature vector into `loan_model.pkl` for inference.

### Request Headers
```http
Content-Type: application/json
```

### Request Body Schema (JSON)

| Field Name | Type | Allowed Values / Constraints | Description |
| :--- | :---: | :--- | :--- |
| `gender` | `string` | `"Male"`, `"Female"` | Applicant's gender |
| `married` | `string` | `"Yes"`, `"No"` | Marital status |
| `dependents` | `string` | `"0"`, `"1"`, `"2"`, `"3+"` | Number of dependents |
| `education` | `string` | `"Graduate"`, `"Not Graduate"` | Educational qualification |
| `self_employed` | `string` | `"Yes"`, `"No"` | Employment classification |
| `applicant_income` | `number` | $\ge 0$ | Primary monthly income |
| `coapplicant_income` | `number` | $\ge 0$ | Secondary/coapplicant monthly income |
| `loan_amount` | `number` | $> 0$ | Loan amount requested (in thousands) |
| `loan_amount_term` | `number` | $> 0$ (e.g., `36`, `60`, `180`, `360`) | Duration of loan term in months |
| `credit_history` | `number` | `1.0` (Good) or `0.0` (Bad) | Credit rating status |
| `property_area` | `string` | `"Rural"`, `"Semiurban"`, `"Urban"` | Location area of property |

### Example Request (Loan Approved)
```json
{
  "gender": "Male",
  "married": "Yes",
  "dependents": "0",
  "education": "Graduate",
  "self_employed": "No",
  "applicant_income": 6500.0,
  "coapplicant_income": 2000.0,
  "loan_amount": 150.0,
  "loan_amount_term": 360.0,
  "credit_history": 1.0,
  "property_area": "Semiurban"
}
```

### Successful Response (Loan Approved)
- Status Code: `200 OK`

```json
{
  "success": true,
  "prediction": "Loan Approved",
  "details": "The machine learning model predicts that this application meets the learned approval pattern."
}
```

### Example Request (Loan Not Approved)
```json
{
  "gender": "Female",
  "married": "No",
  "dependents": "2",
  "education": "Not Graduate",
  "self_employed": "Yes",
  "applicant_income": 1200.0,
  "coapplicant_income": 0.0,
  "loan_amount": 300.0,
  "loan_amount_term": 360.0,
  "credit_history": 0.0,
  "property_area": "Rural"
}
```

### Successful Response (Loan Not Approved)
- Status Code: `200 OK`

```json
{
  "success": true,
  "prediction": "Loan Not Approved",
  "details": "The machine learning model predicts that this application does not meet the learned approval pattern."
}
```

### Validation Error Response (`422 Unprocessable Entity`)
Returned when missing required fields or supplying invalid enum/numeric values.

```json
{
  "detail": [
    {
      "type": "enum",
      "loc": ["body", "gender"],
      "msg": "Input should be 'Male' or 'Female'",
      "input": "InvalidGender"
    }
  ]
}
```

### Server Error Response (`500 Internal Server Error`)
Returned if model inference encounters an internal error. Never leaks Python stack trace.

```json
{
  "success": false,
  "error": "We couldn't process this application. Please verify the information and try again."
}
```
