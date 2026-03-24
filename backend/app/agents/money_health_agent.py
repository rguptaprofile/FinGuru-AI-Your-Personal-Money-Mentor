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
