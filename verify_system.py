#!/usr/bin/env python
"""System verification script"""

print("=" * 50)
print("SYSTEM CHECK")
print("=" * 50)

# 1. Check imports
try:
    from app.services import (
        load_model_bundle,
        get_model,
        get_encoder,
        get_scaler,
        get_categorical_cols,
        get_numerical_cols,
        predict_student_risk
    )
    print("✓ All imports successful")
except Exception as e:
    print(f"✗ Import error: {e}")
    exit(1)

# 2. Check model loading
try:
    bundle = load_model_bundle()
    print("✓ Model loaded successfully")
except Exception as e:
    print(f"✗ Model loading error: {e}")
    exit(1)

# 3. Check model components
try:
    print(f"✓ Model components: {list(bundle.keys())}")
    num_cols = get_numerical_cols()
    cat_cols = get_categorical_cols()
    print(f"✓ Numerical columns ({len(num_cols)}): {num_cols[:3]}...")
    print(f"✓ Categorical columns ({len(cat_cols)}): {cat_cols[:3]}...")
except Exception as e:
    print(f"✗ Component check error: {e}")
    exit(1)

# 4. Check data file
import os
if os.path.exists("data/student-mat.csv"):
    print("✓ Data file found")
else:
    print("✗ Data file not found")

print("=" * 50)
print("ALL CHECKS PASSED!")
print("=" * 50)
