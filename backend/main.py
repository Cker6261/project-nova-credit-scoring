"""
Project Nova - Equitable Credit Scoring Engine
Main FastAPI application for backend services
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
import pandas as pd
import joblib
import os
from datetime import datetime

# Import our custom modules
from models import CreditScoreModel
from database import DatabaseManager
from schema import UserData, UserResponse, ScoreResponse

app = FastAPI(title="Project Nova API", description="Equitable Credit Scoring Engine", version="1.0.0")

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database and ML model
db_manager = DatabaseManager()
credit_model = CreditScoreModel()

@app.on_event("startup")
async def startup_event():
    """Initialize database and ML model on startup"""
    db_manager.initialize_database()
    credit_model.load_or_train_model()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to Project Nova - Equitable Credit Scoring Engine",
        "version": "1.0.0",
        "endpoints": [
            "/calculate_score",
            "/get_users",
            "/get_user/{user_id}"
        ]
    }

def get_risk_category(score: int) -> str:
    """Determine risk category based on credit score"""
    if score >= 700:
        return "Low Risk"
    elif score >= 600:
        return "Medium Risk"
    else:
        return "High Risk"

@app.post("/calculate_score")
async def calculate_score(user_data: UserData):
    """
    Calculate credit score for given user data and save/update user in database
    Returns score, explanations, and user ID
    """
    try:
        # Prepare data for ML model
        features = credit_model.prepare_features(user_data)
        
        # Calculate score using ML model
        score, explanations = credit_model.predict_score(features, user_data)
        
        # Determine risk category
        risk_category = get_risk_category(int(score))
        
        # Prepare user data for database
        user_dict = {
            'name': user_data.name,
            'age': user_data.age,
            'occupation': user_data.occupation,
            'income_level': user_data.income_level.value,
            'monthly_income': user_data.monthly_income,
            'education_level': user_data.education_level,
            'upi_transactions': user_data.upi_transactions,
            'rent_paid_on_time': user_data.rent_paid_on_time,
            'utility_bills_paid': user_data.utility_bills_paid,
            'has_savings_account': user_data.has_savings_account,
            'employment_months': user_data.employment_months,
            'credit_score': int(score),
            'risk_category': risk_category
        }
        
        # Check if user already exists by name
        existing_user_id = db_manager.user_exists_by_name(user_data.name)
        
        if existing_user_id:
            # Update existing user
            db_manager.update_user(existing_user_id, user_dict)
            user_id = existing_user_id
            message = f"User {user_data.name} successfully updated in database"
        else:
            # Add new user to database
            user_id = db_manager.add_user(user_dict)
            message = f"User {user_data.name} successfully added to database"
        
        return {
            "score": int(score),
            "explanations": explanations,
            "calculated_at": datetime.now().isoformat(),
            "user_id": user_id,
            "risk_category": risk_category,
            "message": message
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating score: {str(e)}")

@app.get("/get_users", response_model=List[UserResponse])
async def get_users():
    """
    Get all users with their profiles and scores
    Used by bank dashboard
    """
    try:
        users = db_manager.get_all_users()
        return users
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

@app.put("/update_user/{user_id}")
async def update_user(user_id: int, user_data: UserData):
    """
    Update existing user's credit score and information
    """
    try:
        # Check if user exists
        existing_user = db_manager.get_user_by_id(user_id)
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Calculate new score
        features = credit_model.prepare_features(user_data)
        score, explanations = credit_model.predict_score(features, user_data)
        risk_category = get_risk_category(int(score))
        
        # Update user in database
        user_dict = {
            'name': user_data.name,
            'age': user_data.age,
            'occupation': user_data.occupation,
            'income_level': user_data.income_level.value,
            'monthly_income': user_data.monthly_income,
            'education_level': user_data.education_level,
            'upi_transactions': user_data.upi_transactions,
            'rent_paid_on_time': user_data.rent_paid_on_time,
            'utility_bills_paid': user_data.utility_bills_paid,
            'has_savings_account': user_data.has_savings_account,
            'employment_months': user_data.employment_months,
            'credit_score': int(score),
            'risk_category': risk_category
        }
        
        # Update user in database
        db_manager.update_user(user_id, user_dict)
        
        return {
            "score": int(score),
            "explanations": explanations,
            "calculated_at": datetime.now().isoformat(),
            "user_id": user_id,
            "risk_category": risk_category,
            "message": f"User {user_data.name} successfully updated"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

@app.get("/get_user/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    """
    Get detailed data for a specific user
    Used by user dashboard
    """
    try:
        user = db_manager.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
