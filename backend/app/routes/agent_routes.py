"""
Agent Routes - AI agent interaction endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import Dict, List

router = APIRouter()

@router.post("/money-health-agent")
async def money_health_agent_endpoint(query: Dict):
    """Query Money Health Agent"""
    
    try:
        # Agent will analyze financial data and return health score
        response = {
            "agent": "Money Health Agent",
            "status": "ready",
            "message": "I analyze your financial wellness across 6 dimensions"
        }
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/planning-agent")
async def planning_agent_endpoint(query: Dict):
    """Query Financial Planning Agent"""
    
    try:
        response = {
            "agent": "Financial Planning Agent",
            "status": "ready",
            "message": "I create personalized financial roadmaps with SIP recommendations"
        }
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/tax-agent")
async def tax_agent_endpoint(query: Dict):
    """Query Tax Optimization Agent"""
    
    try:
        response = {
            "agent": "Tax Optimization Agent",
            "status": "ready",
            "message": "I identify tax-saving opportunities and optimize your tax regime"
        }
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/risk-agent")
async def risk_agent_endpoint(query: Dict):
    """Query Risk Analysis Agent"""
    
    try:
        response = {
            "agent": "Risk Analysis Agent",
            "status": "ready",
            "message": "I profile your risk appetite and recommend suitable investments"
        }
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/agents-status")
async def get_agents_status():
    """Get status of all agents"""
    
    return {
        "agents": [
            {
                "name": "Money Health Agent",
                "status": "active",
                "description": "Calculates financial wellness score"
            },
            {
                "name": "Financial Planning Agent",
                "status": "active",
                "description": "Creates financial roadmaps and SIP plans"
            },
            {
                "name": "Tax Optimization Agent",
                "status": "active",
                "description": "Analyzes tax situations and provides optimization"
            },
            {
                "name": "Risk Analysis Agent",
                "status": "active",
                "description": "Profiles risk appetite and recommends investments"
            }
        ]
    }
