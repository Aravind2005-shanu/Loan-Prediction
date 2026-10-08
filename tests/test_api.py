import pytest
from fastapi.testclient import TestClient
from backend.app import app

client = TestClient(app)

def test_get_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "LOAN ELIGIBILITY CHECKER" in response.text

def test_get_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_post_predict_valid_approved():
    payload = {
        "gender": "Male",
        "married": "Yes",
        "dependents": "0",
        "education": "Graduate",
        "self_employed": "No",
        "applicant_income": 7500,
        "coapplicant_income": 2000,
        "loan_amount": 140,
        "loan_amount_term": 360,
        "credit_history": 1.0,
        "property_area": "Urban"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["prediction"] in ["Loan Approved", "Loan Not Approved"]

def test_post_predict_valid_rejected():
    payload = {
        "gender": "Female",
        "married": "No",
        "dependents": "3+",
        "education": "Not Graduate",
        "self_employed": "Yes",
        "applicant_income": 1000,
        "coapplicant_income": 0,
        "loan_amount": 500,
        "loan_amount_term": 360,
        "credit_history": 0.0,
        "property_area": "Rural"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["prediction"] == "Loan Not Approved"

def test_post_predict_missing_field():
    payload = {
        "gender": "Male",
        "married": "Yes"
        # missing other fields
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422  # Unprocessable Entity

def test_post_predict_invalid_enum():
    payload = {
        "gender": "InvalidGender",
        "married": "Yes",
        "dependents": "0",
        "education": "Graduate",
        "self_employed": "No",
        "applicant_income": 5000,
        "coapplicant_income": 0,
        "loan_amount": 100,
        "loan_amount_term": 360,
        "credit_history": 1.0,
        "property_area": "Urban"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
