"""
Quick API Test Script
Run this to test the prediction API
"""

import requests
import json

# Sample student data
sample_student = {
    "school": "GP",
    "sex": "F",
    "age": 17,
    "address": "U",
    "famsize": "GT3",
    "Pstatus": "T",
    "Medu": 4,
    "Fedu": 4,
    "Mjob": "teacher",
    "Fjob": "services",
    "reason": "course",
    "guardian": "mother",
    "traveltime": 2,
    "studytime": 3,
    "failures": 0,
    "schoolsup": "yes",
    "famsup": "no",
    "paid": "no",
    "activities": "yes",
    "nursery": "yes",
    "higher": "yes",
    "internet": "yes",
    "romantic": "no",
    "famrel": 4,
    "freetime": 3,
    "goout": 3,
    "Dalc": 1,
    "Walc": 1,
    "health": 4,
    "absences": 4,
    "G1": 15,
    "G2": 14
}

def test_prediction():
    """Test the prediction endpoint"""
    url = "http://localhost:8000/api/predict"
    
    print("🧪 Testing Student Risk Prediction API...\n")
    print("📊 Sample Student Data:")
    print(json.dumps(sample_student, indent=2))
    print("\n" + "="*50 + "\n")
    
    try:
        response = requests.post(url, json=sample_student)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Prediction Successful!\n")
            print(f"🎯 Risk Level: {result['risk_level']}")
            print(f"📈 Confidence: {result['confidence']}%")
            print(f"💬 Message: {result['message']}")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error!")
        print("Make sure the server is running:")
        print("   python app/main.py")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_health():
    """Test the health endpoint"""
    url = "http://localhost:8000/api/health"
    
    print("\n" + "="*50 + "\n")
    print("🏥 Testing Health Endpoint...\n")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("✅ API is healthy!")
            print(response.json())
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    test_health()
    test_prediction()
    print("\n" + "="*50)
    print("\n🌐 Open http://localhost:8000 in your browser to use the UI!")
