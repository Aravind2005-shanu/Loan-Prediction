import numpy as np
import pandas as pd
from pydantic import BaseModel, Field, field_validator
from typing import Literal

FEATURE_NAMES = [
    'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
    'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term',
    'Credit_History', 'Property_Area'
]

class LoanApplicationRequest(BaseModel):
    gender: Literal["Male", "Female"] = Field(..., description="Gender of the applicant")
    married: Literal["Yes", "No"] = Field(..., description="Marital status of the applicant")
    dependents: Literal["0", "1", "2", "3+"] = Field(..., description="Number of dependents")
    education: Literal["Graduate", "Not Graduate"] = Field(..., description="Educational qualification")
    self_employed: Literal["Yes", "No"] = Field(..., description="Self-employment status")
    applicant_income: float = Field(..., ge=0, description="Applicant monthly income")
    coapplicant_income: float = Field(..., ge=0, description="Co-applicant monthly income")
    loan_amount: float = Field(..., gt=0, description="Loan amount requested (in thousands)")
    loan_amount_term: float = Field(..., gt=0, description="Loan term duration in months")
    credit_history: float = Field(..., description="Credit history guidelines met (1.0 for Yes, 0.0 for No)")
    property_area: Literal["Rural", "Semiurban", "Urban"] = Field(..., description="Property area classification")

    @field_validator("credit_history")
    def validate_credit_history(cls, v: float) -> float:
        if v not in (0.0, 1.0):
            raise ValueError("Credit history must be 0.0 (No/Bad) or 1.0 (Yes/Good)")
        return float(v)

class PredictionResponse(BaseModel):
    success: bool = True
    prediction: str = Field(..., description="'Loan Approved' or 'Loan Not Approved'")
    details: str = Field(..., description="User-friendly status explanation")

def to_feature_vector(data: LoanApplicationRequest) -> pd.DataFrame:
    """
    Transforms validated Pydantic request data into a pandas DataFrame
    matching the exact 11-feature names and order expected by loan_model.pkl:
    ['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed', 
     'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term', 
     'Credit_History', 'Property_Area']
    """
    gender_val = 1.0 if data.gender == "Male" else 0.0
    married_val = 1.0 if data.married == "Yes" else 0.0
    
    dep_map = {"0": 0.0, "1": 1.0, "2": 2.0, "3+": 4.0}
    dependents_val = dep_map[data.dependents]

    education_val = 1.0 if data.education == "Graduate" else 0.0
    self_emp_val = 1.0 if data.self_employed == "Yes" else 0.0
    applicant_income_val = float(data.applicant_income)
    coapplicant_income_val = float(data.coapplicant_income)
    loan_amount_val = float(data.loan_amount)
    loan_term_val = float(data.loan_amount_term)
    credit_hist_val = float(data.credit_history)
    
    prop_map = {"Rural": 0.0, "Semiurban": 1.0, "Urban": 2.0}
    property_area_val = prop_map[data.property_area]

    df = pd.DataFrame([[
        gender_val,
        married_val,
        dependents_val,
        education_val,
        self_emp_val,
        applicant_income_val,
        coapplicant_income_val,
        loan_amount_val,
        loan_term_val,
        credit_hist_val,
        property_area_val
    ]], columns=FEATURE_NAMES)

    return df
