"""
Financial Analysis Routes - Financial planning endpoints
"""
from fastapi import APIRouter, HTTPException, status
from app.agents import MoneyHealthAgent, FinancialPlanningAgent, TaxOptimizationAgent, RiskAnalysisAgent
from typing import Dict, List

router = APIRouter()

# Initialize agents
money_health_agent = MoneyHealthAgent()
financial_planning_agent = FinancialPlanningAgent()
tax_agent = TaxOptimizationAgent()
risk_agent = RiskAnalysisAgent()

@router.post("/money-health-score")
async def calculate_money_health_score(financial_data: Dict):
    """Calculate Money Health Score"""
    
    try:
        score_result = money_health_agent.calculate_score(financial_data)
        return {
            "status": "success",
            "data": score_result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating money health score: {str(e)}"
        )

@router.post("/financial-plan")
async def create_financial_plan(user_data: Dict, goals: List[Dict]):
    """Create comprehensive financial plan"""
    
    try:
        plan = financial_planning_agent.create_financial_plan(user_data, goals)
        return {
            "status": "success",
            "data": plan
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating financial plan: {str(e)}"
        )

@router.post("/tax-analysis")
async def analyze_tax_situation(financial_data: Dict):
    """Analyze tax situation and provide optimization"""
    
    try:
        analysis = tax_agent.analyze_tax_situation(financial_data)
        return {
            "status": "success",
            "data": analysis
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing tax situation: {str(e)}"
        )

@router.post("/risk-profile")
async def profile_user_risk(financial_data: Dict):
    """Profile user risk appetite"""
    
    try:
        risk_profile = risk_agent.profile_risk_appetite(financial_data)
        return {
            "status": "success",
            "data": risk_profile
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error profiling risk: {str(e)}"
        )

@router.post("/full-analysis")
async def full_financial_analysis(user_data: Dict, goals: List[Dict]):
    """Comprehensive financial analysis combining all agents"""
    
    try:
        # Get all analyses
        money_health = money_health_agent.calculate_score(user_data)
        financial_plan = financial_planning_agent.create_financial_plan(user_data, goals)
        tax_analysis = tax_agent.analyze_tax_situation(user_data)
        risk_profile = risk_agent.profile_risk_appetite(user_data)
        
        return {
            "status": "success",
            "data": {
                "money_health_score": money_health,
                "financial_plan": financial_plan,
                "tax_analysis": tax_analysis,
                "risk_profile": risk_profile,
                "summary": {
                    "total_score": money_health["total_score"],
                    "primary_recommendation": financial_plan["recommendations"],
                    "annual_tax_savings_opportunity": tax_analysis["potential_tax_savings"],
                    "risk_level": risk_profile["risk_profile"]
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error performing full analysis: {str(e)}"
        )
