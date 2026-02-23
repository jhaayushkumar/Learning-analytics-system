from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional
import uvicorn
from pathlib import Path

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.predict import predict_student_risk

app = FastAPI(title="Student Risk Analytics", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
static_path = Path(__file__).parent / "static"
static_path.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

class StudentData(BaseModel):
    school: str = Field(..., description="Student's school (GP or MS)")
    sex: str = Field(..., description="Student's sex (F or M)")
    age: int = Field(..., ge=15, le=22, description="Student's age")
    address: str = Field(..., description="Home address type (U=urban or R=rural)")
    famsize: str = Field(..., description="Family size (LE3=<=3 or GT3=>3)")
    Pstatus: str = Field(..., description="Parent's cohabitation status (T=together or A=apart)")
    Medu: int = Field(..., ge=0, le=4, description="Mother's education")
    Fedu: int = Field(..., ge=0, le=4, description="Father's education")
    Mjob: str = Field(..., description="Mother's job")
    Fjob: str = Field(..., description="Father's job")
    reason: str = Field(..., description="Reason to choose this school")
    guardian: str = Field(..., description="Student's guardian")
    traveltime: int = Field(..., ge=1, le=4, description="Home to school travel time")
    studytime: int = Field(..., ge=1, le=4, description="Weekly study time")
    failures: int = Field(..., ge=0, le=4, description="Number of past class failures")
    schoolsup: str = Field(..., description="Extra educational support")
    famsup: str = Field(..., description="Family educational support")
    paid: str = Field(..., description="Extra paid classes")
    activities: str = Field(..., description="Extra-curricular activities")
    nursery: str = Field(..., description="Attended nursery school")
    higher: str = Field(..., description="Wants to take higher education")
    internet: str = Field(..., description="Internet access at home")
    romantic: str = Field(..., description="In a romantic relationship")
    famrel: int = Field(..., ge=1, le=5, description="Quality of family relationships")
    freetime: int = Field(..., ge=1, le=5, description="Free time after school")
    goout: int = Field(..., ge=1, le=5, description="Going out with friends")
    Dalc: int = Field(..., ge=1, le=5, description="Workday alcohol consumption")
    Walc: int = Field(..., ge=1, le=5, description="Weekend alcohol consumption")
    health: int = Field(..., ge=1, le=5, description="Current health status")
    absences: int = Field(..., ge=0, description="Number of school absences")
    G1: int = Field(..., ge=0, le=20, description="First period grade")
    G2: int = Field(..., ge=0, le=20, description="Second period grade")

@app.get("/")
async def read_root():
    return FileResponse(str(static_path / "index.html"))

@app.post("/api/predict")
async def predict(student: StudentData):
    try:
        input_dict = student.dict()
        risk_level, confidence = predict_student_risk(input_dict)
        
        return {
            "success": True,
            "risk_level": risk_level,
            "confidence": confidence,
            "message": f"Student is predicted to be {risk_level} with {confidence}% confidence"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
