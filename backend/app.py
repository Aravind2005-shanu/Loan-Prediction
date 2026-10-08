import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.model_loader import ModelLoader
from backend.validation import LoanApplicationRequest, PredictionResponse
from backend.prediction import predict_loan_eligibility

# Configure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("loan_app.main")

# Determine directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pre-load trained ML model on startup
    logger.info("Initializing Loan Prediction Application...")
    try:
        ModelLoader.load_model()
        logger.info("ML Model pre-loaded successfully.")
    except Exception as e:
        logger.critical(f"Critical error loading ML model on startup: {str(e)}")
    yield
    logger.info("Shutting down Loan Prediction Application...")

app = FastAPI(
    title="Loan Prediction Machine Learning Application",
    description="Production-grade FastAPI application serving real SVM loan approval predictions.",
    version="1.0.0",
    lifespan=lifespan
)

# Enable CORS for local client calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (CSS, JS, assets)
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/", response_class=FileResponse)
async def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="Frontend index.html file not found.")
    return FileResponse(index_path)

@app.get("/health")
async def health_check():
    try:
        model = ModelLoader.get_model()
        if model is None:
            return JSONResponse(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                content={"status": "unhealthy", "detail": "Model is not loaded"}
            )
        return {"status": "healthy"}
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "unhealthy", "detail": "Model loading failed"}
        )

@app.post("/predict", response_model=PredictionResponse)
async def predict_endpoint(data: LoanApplicationRequest):
    try:
        result = predict_loan_eligibility(data)
        return result
    except RuntimeError as re:
        logger.error(f"Prediction runtime error: {str(re)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "We couldn't process this application. Please verify the information and try again."
            }
        )
    except Exception as e:
        logger.error(f"Unexpected prediction exception: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "error": "Internal server error occurred while analyzing the loan application."
            }
        )

# Global exception handler to prevent leaking raw Python stack traces
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "An unexpected error occurred. Please try again later."
        }
    )
