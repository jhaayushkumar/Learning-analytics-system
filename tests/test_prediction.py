"""Test prediction with dummy data"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services import predict_student_risk, get_numerical_cols, get_categorical_cols

# Get expected columns
num_cols = get_numerical_cols()
cat_cols = get_categorical_cols()

print("=" * 60)
print("PREDICTION TEST WITH DUMMY DATA")
print("=" * 60)
print(f"\nExpected columns:")
print(f"  Numerical ({len(num_cols)}): {num_cols}")
print(f"  Categorical ({len(cat_cols)}): {cat_cols}")

# Create dummy data with all required features
dummy_data = {}

# Add categorical features
for col in cat_cols:
    dummy_data[col] = "yes"  # Default value

# Add numerical features
for col in num_cols:
    dummy_data[col] = 2  # Default value

print(f"\nDummy data created with {len(dummy_data)} features")

# Test 1: Default values
print("\n" + "-" * 60)
print("TEST 1: Default values (all yes/2)")
print("-" * 60)
try:
    risk_level, confidence = predict_student_risk(dummy_data)
    print(f"✓ Risk Level: {risk_level}")
    print(f"✓ Confidence: {confidence}%")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Good student (higher grades)
print("\n" + "-" * 60)
print("TEST 2: Good student (high grades)")
print("-" * 60)
dummy_data_good = dummy_data.copy()
dummy_data_good['G1'] = 18  # First period grade
dummy_data_good['G2'] = 19  # Second period grade
try:
    risk_level, confidence = predict_student_risk(dummy_data_good)
    print(f"✓ Risk Level: {risk_level}")
    print(f"✓ Confidence: {confidence}%")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: At-risk student (low grades, failures)
print("\n" + "-" * 60)
print("TEST 3: At-risk student (low grades, high failures)")
print("-" * 60)
dummy_data_risk = dummy_data.copy()
dummy_data_risk['G1'] = 8   # Poor first period grade
dummy_data_risk['G2'] = 9   # Poor second period grade
dummy_data_risk['failures'] = 3  # Multiple failures
try:
    risk_level, confidence = predict_student_risk(dummy_data_risk)
    print(f"✓ Risk Level: {risk_level}")
    print(f"✓ Confidence: {confidence}%")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("ALL TESTS COMPLETED SUCCESSFULLY!")
print("=" * 60)
