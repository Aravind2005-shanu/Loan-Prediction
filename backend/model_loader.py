import os
import pickle
from typing import Any
import logging

logger = logging.getLogger("loan_app.model_loader")

class ModelLoader:
    _instance = None
    _model: Any = None

    @classmethod
    def get_model_path(cls) -> str:
        # Determine path to loan_model.pkl relative to project root
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(current_dir, ".."))
        model_path = os.path.join(project_root, "loan_model.pkl")
        return model_path

    @classmethod
    def load_model(cls) -> Any:
        if cls._model is None:
            model_path = cls.get_model_path()
            if not os.path.exists(model_path):
                logger.error(f"Model file not found at path: {model_path}")
                raise FileNotFoundError(f"Model file 'loan_model.pkl' not found at {model_path}")
            
            try:
                with open(model_path, "rb") as f:
                    cls._model = pickle.load(f)
                logger.info(f"Successfully loaded loan model from {model_path}")
            except Exception as e:
                logger.error(f"Failed to unpickle model: {str(e)}")
                raise RuntimeError(f"Error loading trained model: {str(e)}")
                
        return cls._model

    @classmethod
    def get_model(cls) -> Any:
        if cls._model is None:
            return cls.load_model()
        return cls._model
