"""
Agents - Initialize all AI agents
"""
from .money_health_agent import MoneyHealthAgent
from .financial_planning_agent import FinancialPlanningAgent
from .tax_agent import TaxOptimizationAgent
from .risk_agent import RiskAnalysisAgent

__all__ = [
    "MoneyHealthAgent",
    "FinancialPlanningAgent",
    "TaxOptimizationAgent",
    "RiskAnalysisAgent"
]
