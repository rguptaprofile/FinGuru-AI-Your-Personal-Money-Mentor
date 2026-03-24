"""
Financial Planning Agent - Creates comprehensive financial roadmaps and SIP plans
"""
import os
from typing import Dict, List
from openai import OpenAI
import json

class FinancialPlanningAgent:
    """
    Financial Planning Agent
    Generates:
    - SIP recommendations
    - Asset allocation strategy
    - Goal-based investment plans
    - Financial roadmap
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
    
    def create_financial_plan(self, user_data: Dict, goals: List[Dict]) -> Dict:
        """Create comprehensive financial plan"""
        
        # Calculate SIP plans for each goal
        sip_plans = self._calculate_sip_for_goals(user_data, goals)
        
        # Generate asset allocation
        asset_allocation = self._generate_asset_allocation(
            user_data.get("risk_profile", "Moderate"),
            user_data.get("age", 30)
        )
        
        # Get AI recommendations
        recommendations = self._get_plan_recommendations(
            user_data, goals, sip_plans, asset_allocation
        )
        
        return {
            "sip_recommendations": sip_plans,
            "asset_allocation": asset_allocation,
            "recommendations": recommendations,
            "risk_profile": user_data.get("risk_profile"),
            "investment_horizon_years": 30 - (user_data.get("age", 30) - 25)
        }
    
    def _calculate_sip_for_goals(self, user_data: Dict, goals: List[Dict]) -> Dict:
        """Calculate SIP amount needed for each goal"""
        
        sip_plans = {}
        annual_income = user_data.get("annual_income", 0)
        
        for goal in goals:
            target_amount = goal.get("target_amount", 0)
            target_year = goal.get("target_year", 2030)
            years_remaining = target_year - 2024
            
            # Assume 12% annual return
            expected_return = 0.12
            monthly_rate = (1 + expected_return) ** (1/12) - 1
            
            # FV = PMT × [((1 + r)^n - 1) / r]
            # Solve for PMT
            if years_remaining > 0 and monthly_rate > 0:
                months = years_remaining * 12
                sip_amount = target_amount / (((1 + monthly_rate) ** months - 1) / monthly_rate)
            else:
                sip_amount = target_amount / 12
            
            # Calculate as % of annual income
            sip_percentage = (sip_amount * 12) / annual_income * 100 if annual_income > 0 else 0
            
            sip_plans[goal.get("goal_name")] = {
                "monthly_sip": round(sip_amount, 2),
                "annual_sip": round(sip_amount * 12, 2),
                "percentage_of_income": round(sip_percentage, 2),
                "duration_months": months,
                "target_amount": target_amount,
                "expected_value": round(target_amount * 1.12 ** years_remaining, 2),
                "priority": goal.get("priority", 3)
            }
        
        return sip_plans
    
    def _generate_asset_allocation(self, risk_profile: str, age: int) -> Dict:
        """Generate recommended asset allocation"""
        
        allocation_matrix = {
            "Conservative": {
                "equity": 30,
                "debt": 50,
                "gold": 10,
                "cash": 10
            },
            "Moderate": {
                "equity": 60,
                "debt": 25,
                "gold": 10,
                "cash": 5
            },
            "Aggressive": {
                "equity": 80,
                "debt": 10,
                "gold": 5,
                "cash": 5
            }
        }
        
        base_allocation = allocation_matrix.get(risk_profile, allocation_matrix["Moderate"])
        
        # Adjust based on age
        years_to_retirement = max(0, 60 - age)
        age_factor = years_to_retirement / 30
        
        return {
            "equity": round(base_allocation["equity"] * (0.8 + 0.2 * age_factor), 2),
            "debt": round(base_allocation["debt"] * (1 - 0.1 * age_factor), 2),
            "gold": base_allocation["gold"],
            "cash": base_allocation["cash"],
            "recommended_funds": [
                {"name": "Nifty 50", "type": "equity", "allocation": 30},
                {"name": "Balanced Fund", "type": "hybrid", "allocation": 20},
                {"name": "Government Securities", "type": "debt", "allocation": 25},
                {"name": "Sovereign Gold Bond", "type": "gold", "allocation": 10}
            ]
        }
    
    def _get_plan_recommendations(self, user_data, goals, sip_plans, allocation):
        """Get AI-powered planning recommendations"""
        
        prompt = f"""
        Create a financial planning recommendation for a user with:
        - Age: {user_data.get('age')}
        - Annual Income: ₹{user_data.get('annual_income')}
        - Monthly Expenses: ₹{user_data.get('monthly_expenses')}
        - Risk Profile: {user_data.get('risk_profile')}
        - Debt: ₹{user_data.get('debt_amount')}
        
        Goals: {json.dumps(goals)}
        Recommended Asset Allocation: {json.dumps(allocation)}
        
        Provide 4-5 specific, actionable recommendations for this user.
        Include investment vehicles, timeline, and expected outcomes.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return "Focus on consistent SIP investments and debt reduction"
