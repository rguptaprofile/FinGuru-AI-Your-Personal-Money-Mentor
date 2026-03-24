"""
User Routes - User management endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.user import UserProfile, UserRequest, FinancialInput, FinancialGoal
from datetime import datetime

router = APIRouter()

# In-memory storage (replace with database in production)
users_db = {}
financial_data_db = {}
goals_db = {}

@router.post("/register")
async def register_user(user_data: UserRequest):
    """Register a new user"""
    
    # Check if user already exists
    if user_data.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already registered"
        )
    
    user_id = f"user_{datetime.now().timestamp()}"
    
    user = UserProfile(
        user_id=user_id,
        name=user_data.name,
        email=user_data.email,
        age=user_data.age,
        gender=user_data.gender,
        phone=user_data.phone
    )
    
    users_db[user_data.email] = user.dict()
    
    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "email": user_data.email
    }

@router.get("/profile/{email}")
async def get_user_profile(email: str):
    """Get user profile"""
    
    if email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return users_db[email]

@router.post("/financial-input")
async def add_financial_input(financial_input: FinancialInput):
    """Add or update user financial information"""
    
    user_id = financial_input.user_id
    
    financial_data_db[user_id] = financial_input.dict()
    
    return {
        "message": "Financial data saved successfully",
        "user_id": user_id
    }

@router.get("/financial-input/{user_id}")
async def get_financial_input(user_id: str):
    """Get user financial information"""
    
    if user_id not in financial_data_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Financial data not found"
        )
    
    return financial_data_db[user_id]

@router.post("/goals")
async def create_goal(goal: FinancialGoal):
    """Create a financial goal"""
    
    user_id = goal.user_id
    
    if user_id not in goals_db:
        goals_db[user_id] = []
    
    goals_db[user_id].append(goal.dict())
    
    return {
        "message": "Goal created successfully",
        "goal_id": goal.goal_id
    }

@router.get("/goals/{user_id}")
async def get_user_goals(user_id: str):
    """Get all goals for a user"""
    
    if user_id not in goals_db:
        return {"goals": []}
    
    return {"goals": goals_db[user_id]}

@router.delete("/goals/{goal_id}")
async def delete_goal(goal_id: str):
    """Delete a goal"""
    
    for user_id in goals_db:
        goals_db[user_id] = [g for g in goals_db[user_id] if g["goal_id"] != goal_id]
    
    return {"message": "Goal deleted successfully"}
