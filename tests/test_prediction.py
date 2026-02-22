import pytest
from app.services.prediction_service import make_prediction

def test_make_prediction():
    # Example input for testing
    input_data = {
        "feature1": 1.0,
        "feature2": 2.0,
        "feature3": 3.0,
        # Add other features as required by the model
    }
    
    prediction = make_prediction(input_data)
    
    # Assert that the prediction is as expected
    assert prediction is not None
    # Add more specific assertions based on expected output
    # For example:
    # assert prediction['risk_level'] in ['low', 'medium', 'high']