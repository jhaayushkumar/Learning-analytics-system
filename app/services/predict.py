import pandas as pd
import numpy as np
from .model_loader import (
    get_model,
    get_encoder,
    get_scaler,
    get_categorical_cols,
    get_numerical_cols
)

def predict_student_risk(input_data: dict):
    """Predict risk using saved model bundle"""
    model = get_model()
    encoder = get_encoder()
    scaler = get_scaler()
    categorical_cols = get_categorical_cols()
    numerical_cols = get_numerical_cols()
    
    # Convert input to DataFrame
    df = pd.DataFrame([input_data])
    
    # Split columns
    X_num = df[numerical_cols]
    X_cat = df[categorical_cols]
    
    # Apply transformations
    X_num_scaled = scaler.transform(X_num)
    X_cat_encoded = encoder.transform(X_cat)
    
    # Combine
    X_final = np.hstack([X_num_scaled, X_cat_encoded])
    
    # Predict
    prediction = model.predict(X_final)[0]
    probability = model.predict_proba(X_final).max()
    
    # Map readable label
    risk_map = {
        0: "At-risk",
        1: "Average",
        2: "High-performing"
    }
    
    return risk_map[prediction], round(probability * 100, 2)
