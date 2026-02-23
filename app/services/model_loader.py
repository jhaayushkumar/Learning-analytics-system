import joblib
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "student_risk_models.pkl"

# Cache for model bundle
_model_bundle = None

def load_model_bundle():
    global _model_bundle
    
    if _model_bundle is None:
        _model_bundle = joblib.load(MODEL_PATH)
        print("Model loaded successfully!")
    
    return _model_bundle

def get_logistic_model():
    return load_model_bundle()["logistic_model"]

def get_decision_tree_model():
    return load_model_bundle()["decision_tree_model"]

def get_encoder():
    return load_model_bundle()["encoder"]

def get_scaler():
    return load_model_bundle()["scaler"]

def get_categorical_cols():
    return load_model_bundle()["categorical_cols"]

def get_numerical_cols():
    return load_model_bundle()["numerical_cols"]
