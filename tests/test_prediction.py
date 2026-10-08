import pytest
import numpy as np
import pandas as pd
from backend.model_loader import ModelLoader
from backend.validation import LoanApplicationRequest, to_feature_vector
from backend.prediction import predict_loan_eligibility

def test_model_loading():
    model = ModelLoader.get_model()
    assert model is not None, "Model should be loaded successfully"
    assert hasattr(model, "predict"), "Loaded model must have a predict method"

def test_feature_vector_conversion():
    req = LoanApplicationRequest(
        gender="Male",
        married="Yes",
        dependents="1",
        education="Graduate",
        self_employed="No",
        applicant_income=6000.0,
        coapplicant_income=1500.0,
        loan_amount=200.0,
        loan_amount_term=360.0,
        credit_history=1.0,
        property_area="Urban"
    )
    df = to_feature_vector(req)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (1, 11)
    assert list(df.columns) == [
        'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
        'Credit_History', 'Property_Area'
    ]
    
    expected = [1.0, 1.0, 1.0, 1.0, 0.0, 6000.0, 1500.0, 200.0, 360.0, 1.0, 2.0]
    np.testing.assert_array_equal(df.values[0], expected)

def test_prediction_approved_case():
    req = LoanApplicationRequest(
        gender="Male",
        married="Yes",
        dependents="0",
        education="Graduate",
        self_employed="No",
        applicant_income=8000.0,
        coapplicant_income=2500.0,
        loan_amount=150.0,
        loan_amount_term=360.0,
        credit_history=1.0,
        property_area="Semiurban"
    )
    res = predict_loan_eligibility(req)
    assert res.success is True
    assert res.prediction == "Loan Approved"

def test_prediction_rejected_case():
    req = LoanApplicationRequest(
        gender="Female",
        married="No",
        dependents="2",
        education="Not Graduate",
        self_employed="Yes",
        applicant_income=1200.0,
        coapplicant_income=0.0,
        loan_amount=350.0,
        loan_amount_term=360.0,
        credit_history=0.0,
        property_area="Rural"
    )
    res = predict_loan_eligibility(req)
    assert res.success is True
    assert res.prediction == "Loan Not Approved"
