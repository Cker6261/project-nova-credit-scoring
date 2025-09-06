"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class IncomeLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class UserData(BaseModel):
    """Input schema for credit score calculation"""
    name: str
    age: int
    occupation: str
    income_level: IncomeLevel
    monthly_income: float
    education_level: int  # 1-5 scale
    upi_transactions: int  # Number of UPI transactions per month
    rent_paid_on_time: bool  # 0 or 1
    utility_bills_paid: bool  # 0 or 1
    has_savings_account: bool = True
    employment_months: int = 12  # Months in current employment

class UserResponse(BaseModel):
    """Response schema for user data"""
    id: int
    name: str
    age: int
    occupation: str
    income_level: str
    monthly_income: float
    education_level: int
    upi_transactions: int
    rent_paid_on_time: bool
    utility_bills_paid: bool
    has_savings_account: bool
    employment_months: int
    credit_score: int
    risk_category: str

class ScoreResponse(BaseModel):
    """Response schema for credit score calculation"""
    score: int
    explanations: List[str]
    calculated_at: str

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
