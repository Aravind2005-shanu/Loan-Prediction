import logging
from backend.model_loader import ModelLoader
from backend.validation import LoanApplicationRequest, PredictionResponse, to_feature_vector

logger = logging.getLogger("loan_app.prediction")

def predict_loan_eligibility(request_data: LoanApplicationRequest) -> PredictionResponse:
    """
    Executes real inference on loan_model.pkl using the formatted feature vector.
    Returns structured PredictionResponse.
    """
    try:
        model = ModelLoader.get_model()
        features = to_feature_vector(request_data)
        
        # Perform prediction using trained SVM model
        raw_prediction = model.predict(features)
        prediction_val = int(raw_prediction[0])

        if prediction_val == 1:
            prediction_text = "Loan Approved"
            details_text = "The machine learning model predicts that this application meets the learned approval pattern."
        else:
            prediction_text = "Loan Not Approved"
            details_text = "The machine learning model predicts that this application does not meet the learned approval pattern."

        return PredictionResponse(
            success=True,
            prediction=prediction_text,
            details=details_text
        )
    except Exception as e:
        logger.error(f"Prediction engine execution error: {str(e)}", exc_info=True)
        raise RuntimeError("An error occurred during machine learning model inference.")
