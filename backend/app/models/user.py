"""
User Models - Pydantic schemas for user data
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserProfile(BaseModel):
    """User Financial Profile"""
    user_id: str
    name: str
    email: EmailStr
    age: int
    gender: Optional[str] = None
    phone: Optional[str] = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

class FinancialInput(BaseModel):
    """User Financial Input Data"""
    user_id: str
    monthly_income: float
    annual_income: float
    monthly_expenses: float
    annual_expenses: float
    existing_savings: float
    existing_investments: float
    debt_amount: float
    emergency_fund_target: float
    risk_profile: str  # Conservative, Moderate, Aggressive
    
class FinancialGoal(BaseModel):
    """Financial Goal Data"""
    goal_id: str
    user_id: str
    goal_name: str
    goal_type: str  # House, Car, Vacation, Retirement, Education, etc.
    target_amount: float
    target_year: int
    priority: int  # 1=High, 2=Medium, 3=Low
    created_at: datetime = datetime.now()

class UserRequest(BaseModel):
    """User Profile Creation Request"""
    name: str
    email: EmailStr
    age: int
    gender: Optional[str] = None
    phone: Optional[str] = None
