"""
Financial Models - Financial calculation models
"""
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime

class MoneyHealthScore(BaseModel):
    """Money Health Score Response"""
    total_score: int  # 0-100
    score_breakdown: Dict[str, int]  # 6 dimensions: emergency, insurance, diversification, debt, tax, retirement
    recommendation: str
    priority_actions: List[str]

class SIPPlan(BaseModel):
    """Systematic Investment Plan"""
    monthly_sip: float
    duration_months: int
    target_amount: float
    expected_return_rate: float
    total_investment: float
    expected_value: float
    inflation_adjusted: float

class TaxOptimizationResult(BaseModel):
    """Tax Optimization Analysis"""
    current_tax: float
    optimized_tax: float
    tax_savings: float
    savings_percentage: float
    deductions_missed: List[Dict[str, str]]
    regime_recommendation: str  # Old or New
    suggestions: List[str]

class InvestmentRecommendation(BaseModel):
    """AI Investment Recommendation"""
    recommendation_id: str
    user_id: str
    recommendation_type: str  # MF, SIP, Insurance, NPS, etc.
    products: List[Dict[str, str]]
    reasoning: str
    expected_return: float
    risk_level: str
    created_at: datetime = datetime.now()

class PortfolioAnalysis(BaseModel):
    """Portfolio X-Ray Analysis"""
    total_portfolio_value: float
    xirr: float
    allocation_breakdown: Dict[str, float]
    overlap_percentage: float
    expense_ratio_drag: float
    benchmark_comparison: float
    rebalancing_suggestions: List[str]

class FinancialRoadmap(BaseModel):
    """Complete Financial Roadmap"""
    user_id: str
    current_status: Dict
    goals: List[Dict]
    sip_recommendations: Dict
    asset_allocation: Dict
    tax_strategy: Dict
    insurance_gaps: List[str]
    emergency_fund_plan: Dict
    monthly_budget_plan: Dict
    created_at: datetime = datetime.now()
