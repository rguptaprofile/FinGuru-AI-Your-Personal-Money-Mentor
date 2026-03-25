from app.models.schemas import MoneyHealthDimension, MoneyHealthResponse, ProfileInput


def _clamp_score(score: float) -> int:
    return max(0, min(100, round(score)))


def evaluate_money_health(profile: ProfileInput) -> MoneyHealthResponse:
    monthly_surplus = profile.monthly_income - profile.monthly_expenses - profile.monthly_emi
    emergency_target = profile.monthly_expenses * 6

    emergency_score = _clamp_score((profile.emergency_fund / max(1, emergency_target)) * 100)
    insurance_needed = profile.annual_salary * 15
    insurance_score = _clamp_score((profile.annual_insurance_cover / max(1, insurance_needed)) * 100)

    invest_ratio = profile.existing_investments / max(1, profile.annual_salary)
    diversification_score = _clamp_score(30 + invest_ratio * 70)

    debt_to_income = (profile.monthly_emi / max(1, profile.monthly_income)) * 100
    debt_health_score = _clamp_score(100 - (debt_to_income * 2))

    savings_ratio = (monthly_surplus / max(1, profile.monthly_income)) * 100
    tax_efficiency_score = _clamp_score(40 + max(0, savings_ratio) * 1.5)

    retirement_score = _clamp_score((profile.existing_investments / max(1, profile.annual_salary * 2)) * 100)

    dimensions = [
        MoneyHealthDimension(
            name="Emergency Preparedness",
            score=emergency_score,
            insight=f"Emergency fund covers {profile.emergency_fund / max(1, profile.monthly_expenses):.1f} months.",
        ),
        MoneyHealthDimension(
            name="Insurance Coverage",
            score=insurance_score,
            insight=f"Current cover is {round((profile.annual_insurance_cover / max(1, insurance_needed)) * 100)}% of recommended.",
        ),
        MoneyHealthDimension(
            name="Investment Diversification",
            score=diversification_score,
            insight="Diversify across index funds, debt funds, and gold ETFs.",
        ),
        MoneyHealthDimension(
            name="Debt Health",
            score=debt_health_score,
            insight=f"EMI to income ratio is {debt_to_income:.1f}%.",
        ),
        MoneyHealthDimension(
            name="Tax Efficiency",
            score=tax_efficiency_score,
            insight="Use 80C, 80D, and HRA to improve post-tax returns.",
        ),
        MoneyHealthDimension(
            name="Retirement Readiness",
            score=retirement_score,
            insight="Step up SIP by 10% annually for faster FIRE progress.",
        ),
    ]

    total_score = round(sum(item.score for item in dimensions) / len(dimensions))
    if total_score >= 75:
        status = "Strong"
    elif total_score >= 50:
        status = "Stable but needs improvement"
    else:
        status = "At risk"

    recommendations = [
        "Build emergency corpus to 6 months of expenses.",
        "Keep EMI below 30% of monthly income.",
        "Increase SIP by at least 10% every year.",
        "Review insurance and tax deductions each financial year.",
    ]

    return MoneyHealthResponse(
        total_score=total_score,
        status=status,
        dimensions=dimensions,
        recommendations=recommendations,
    )
"""
Money Health Agent - Calculates comprehensive financial wellness score
"""
import os
from typing import Dict, List
from openai import OpenAI

class MoneyHealthAgent:
    """
    Money Health Score Agent
    Scores users across 6 dimensions:
    1. Emergency Preparedness (savings coverage)
    2. Insurance Coverage (coverage gaps)
    3. Investment Diversification
    4. Debt Health
    5. Tax Efficiency
    6. Retirement Readiness
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    def calculate_score(self, financial_data: Dict) -> Dict:
        """Calculate Money Health Score"""
        
        # Extract key metrics
        monthly_expenses = financial_data.get("monthly_expenses", 0)
        emergency_fund = financial_data.get("existing_savings", 0)
        annual_income = financial_data.get("annual_income", 0)
        debt = financial_data.get("debt_amount", 0)
        investments = financial_data.get("existing_investments", 0)
        age = financial_data.get("age", 30)
        
        # Calculate 6 dimensions
        scores = self._calculate_dimensions(
            monthly_expenses, emergency_fund, annual_income, 
            debt, investments, age
        )
        
        total_score = sum(scores.values()) // 6
        
        # Get AI-generated recommendations
        recommendations = self._get_ai_recommendations(
            scores, financial_data, total_score
        )
        
        return {
            "total_score": total_score,
            "score_breakdown": scores,
            "recommendations": recommendations["priority_actions"],
            "recommendation": recommendations["summary"]
        }
    
    def _calculate_dimensions(self, monthly_expenses, emergency_fund, 
                              annual_income, debt, investments, age):
        """Calculate individual dimension scores"""
        
        # 1. Emergency Preparedness (max 6 months expenses)
        months_covered = emergency_fund / monthly_expenses if monthly_expenses > 0 else 0
        emergency_score = min(20, int((months_covered / 6) * 20))
        
        # 2. Insurance Coverage (simplified)
        insurance_coverage = min(20, int((annual_income / 100000) * 20))
        
        # 3. Investment Diversification
        diversification_score = 0
        if investments > 0:
            diversification_score = min(20, 15)  # Placeholder
        
        # 4. Debt Health (lower is better)
        debt_ratio = (debt / annual_income * 100) if annual_income > 0 else 100
        debt_score = max(0, 20 - int(debt_ratio / 5))
        
        # 5. Tax Efficiency (assumed)
        tax_score = 15  # Needs form 16 to calculate properly
        
        # 6. Retirement Readiness
        retirement_savings_needed = annual_income * (60 - age) * 0.7
        retirement_score = min(20, int((investments / retirement_savings_needed * 100) / 5)) if retirement_savings_needed > 0 else 10
        
        return {
            "emergency_preparedness": emergency_score,
            "insurance_coverage": insurance_coverage,
            "investment_diversification": diversification_score,
            "debt_health": debt_score,
            "tax_efficiency": tax_score,
            "retirement_readiness": retirement_score
        }
    
    def _get_ai_recommendations(self, scores, financial_data, total_score):
        """Get AI-powered recommendations"""
        
        prompt = f"""
        Based on the following Money Health Score breakdown:
        {scores}
        
        And financial data:
        - Age: {financial_data.get('age')}
        - Annual Income: ₹{financial_data.get('annual_income')}
        - Monthly Expenses: ₹{financial_data.get('monthly_expenses')}
        - Existing Savings: ₹{financial_data.get('existing_savings')}
        - Debt: ₹{financial_data.get('debt_amount')}
        
        Provide 3-4 priority actions to improve financial health. Be specific and actionable.
        Format response as JSON with "summary" and "priority_actions" array.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"Error getting AI recommendations: {e}")
            return {
                "summary": "Focus on emergency fund and investment diversification",
                "priority_actions": [
                    "Build emergency fund to 6 months of expenses",
                    "Diversify investments across asset classes",
                    "Optimize tax savings through SIP and insurance"
                ]
            }
