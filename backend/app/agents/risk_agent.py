"""
Risk Analysis Agent - Profiles user risk and recommends appropriate investments
"""
import os
from typing import Dict, List
from openai import OpenAI

class RiskAnalysisAgent:
    """
    Risk Analysis Agent
    Profiles user risk appetite and recommends suitable investments
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    def profile_risk_appetite(self, financial_data: Dict) -> Dict:
        """Analyze user's risk appetite"""
        
        # Calculate risk metrics
        age = financial_data.get("age", 30)
        years_to_retirement = 60 - age
        
        # Emergency fund ratio
        emergency_fund = financial_data.get("existing_savings", 0)
        monthly_expenses = financial_data.get("monthly_expenses", 0)
        emergency_ratio = (emergency_fund / (monthly_expenses * 6)) if monthly_expenses > 0 else 0
        
        # Debt-to-income ratio
        debt = financial_data.get("debt_amount", 0)
        annual_income = financial_data.get("annual_income", 0)
        debt_ratio = (debt / annual_income) if annual_income > 0 else 0
        
        # Savings rate
        monthly_income = annual_income / 12
        monthly_surplus = monthly_income - monthly_expenses
        savings_rate = (monthly_surplus / monthly_income) if monthly_income > 0 else 0
        
        # Calculate risk score (100 = very aggressive, 0 = very conservative)
        risk_score = self._calculate_risk_score(
            age, years_to_retirement, emergency_ratio, debt_ratio, savings_rate
        )
        
        risk_profile = self._determine_risk_profile(risk_score)
        
        recommendations = self._get_risk_recommendations(
            risk_profile, financial_data
        )
        
        return {
            "risk_score": round(risk_score, 2),
            "risk_profile": risk_profile,
            "risk_factors": {
                "years_to_retirement": years_to_retirement,
                "emergency_fund_coverage": round(emergency_ratio, 2),
                "debt_to_income_ratio": round(debt_ratio, 2),
                "monthly_savings_rate": f"{round(savings_rate * 100, 1)}%"
            },
            "investment_recommendations": recommendations
        }
    
    def _calculate_risk_score(self, age, years_to_retirement, emergency_ratio, 
                             debt_ratio, savings_rate):
        """Calculate composite risk score"""
        
        score = 50  # Base score
        
        # Age factor: Younger = can take more risk
        if age < 30:
            score += 15
        elif age < 40:
            score += 10
        elif age < 50:
            score += 5
        else:
            score -= 10
        
        # Emergency fund factor: Good coverage = can take more risk
        if emergency_ratio >= 1:
            score += 10
        elif emergency_ratio >= 0.5:
            score += 5
        else:
            score -= 10
        
        # Debt factor: Low debt = can take more risk
        if debt_ratio < 0.5:
            score += 10
        elif debt_ratio < 1:
            score += 5
        else:
            score -= 15
        
        # Savings rate: Good savings = can take more risk
        if savings_rate > 0.3:
            score += 10
        elif savings_rate > 0.15:
            score += 5
        else:
            score -= 5
        
        return max(0, min(100, score))
    
    def _determine_risk_profile(self, risk_score):
        """Determine risk profile based on score"""
        
        if risk_score >= 70:
            return "Aggressive"
        elif risk_score >= 40:
            return "Moderate"
        else:
            return "Conservative"
    
    def _get_risk_recommendations(self, risk_profile: str, financial_data: Dict):
        """Get investment recommendations based on risk profile"""
        
        recommendations = {
            "Conservative": {
                "equity_allocation": 30,
                "debt_allocation": 50,
                "gold_allocation": 10,
                "cash_allocation": 10,
                "investment_vehicles": [
                    {"name": "Senior Citizen Savings Scheme", "type": "debt", "description": "8.2% p.a., safe"},
                    {"name": "Government Securities", "type": "debt", "description": "Secure, regular returns"},
                    {"name": "Debt Mutual Funds", "type": "debt", "description": "Better than FDs, tax efficient"},
                    {"name": "Balanced Funds", "type": "hybrid", "description": "Stable with growth"}
                ],
                "risk_warning": "Your portfolio is designed for capital preservation. Long-term growth may be limited.",
                "action": "Review annually and shift to growth once emergency fund is secured"
            },
            "Moderate": {
                "equity_allocation": 60,
                "debt_allocation": 25,
                "gold_allocation": 10,
                "cash_allocation": 5,
                "investment_vehicles": [
                    {"name": "Large Cap Funds", "type": "equity", "description": "Stable, liquid"},
                    {"name": "Mid Cap Funds", "type": "equity", "description": "Growth potential"},
                    {"name": "Balanced Funds", "type": "hybrid", "description": "Diversified approach"},
                    {"name": "Debt Funds", "type": "debt", "description": "Stability component"}
                ],
                "risk_warning": "Moderate volatility expected. Stay invested for 5+ years.",
                "action": "SIP approach recommended. Rebalance annually."
            },
            "Aggressive": {
                "equity_allocation": 80,
                "debt_allocation": 10,
                "gold_allocation": 5,
                "cash_allocation": 5,
                "investment_vehicles": [
                    {"name": "Small Cap Funds", "type": "equity", "description": "High growth potential"},
                    {"name": "Mid Cap Funds", "type": "equity", "description": "Strong growth"},
                    {"name": "Large Cap Funds", "type": "equity", "description": "Quality picks"},
                    {"name": "Emerging Themes Fund", "type": "equity", "description": "Future growth"},
                    {"name": "International Funds", "type": "equity", "description": "Diversification"}
                ],
                "risk_warning": "High volatility expected. Only for 10+ year horizon.",
                "action": "Regular rebalancing needed. Stay disciplined during market downturns."
            }
        }
        
        return recommendations.get(risk_profile, recommendations["Moderate"])
