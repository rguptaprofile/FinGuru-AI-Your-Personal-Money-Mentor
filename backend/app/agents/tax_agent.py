"""
Tax Optimization Agent - Analyzes tax situations and recommends optimization strategies
"""
import os
from typing import Dict, List
from openai import OpenAI
import json

class TaxOptimizationAgent:
    """
    Tax Optimization Agent
    Analyzes:
    - Old vs New tax regime
    - 80C deductions
    - HRA optimization
    - NPS contributions
    - Loss harvesting opportunities
    """
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key) if api_key else None
        self.model = os.getenv("OPENAI_MODEL", "gpt-4")
        self.tax_year = 2024
    
    def analyze_tax_situation(self, financial_data: Dict) -> Dict:
        """Analyze tax situation and provide optimization"""
        
        gross_income = financial_data.get("annual_income", 0)
        
        # Calculate taxes under both regimes
        old_regime_tax = self._calculate_old_regime_tax(gross_income, financial_data)
        new_regime_tax = self._calculate_new_regime_tax(gross_income)
        
        # Identify missing deductions
        missed_deductions = self._identify_missed_deductions(financial_data)
        
        # Get AI optimization suggestions
        suggestions = self._get_optimization_suggestions(
            financial_data, old_regime_tax, new_regime_tax, missed_deductions
        )
        
        tax_savings = abs(old_regime_tax - new_regime_tax)
        
        return {
            "gross_income": gross_income,
            "old_regime_tax": old_regime_tax,
            "new_regime_tax": new_regime_tax,
            "recommended_regime": "Old" if old_regime_tax < new_regime_tax else "New",
            "potential_tax_savings": tax_savings,
            "missed_deductions": missed_deductions,
            "optimization_suggestions": suggestions,
            "hra_optimization": self._optimize_hra(financial_data),
            "nps_recommendation": self._recommend_nps(financial_data)
        }
    
    def _calculate_old_regime_tax(self, gross_income: float, financial_data: Dict) -> float:
        """Calculate tax under old regime with deductions"""
        
        # Calculate deductions
        section_80c = min(150000, financial_data.get("sip_annual", 0) + financial_data.get("insurance_premium", 0))
        section_80d = financial_data.get("health_insurance", 0)
        section_80e = financial_data.get("education_loan_interest", 0)
        section_80g = financial_data.get("charitable_donations", 0)
        
        # Standard deduction
        standard_deduction = 50000
        
        total_deductions = section_80c + section_80d + section_80e + section_80g + standard_deduction
        taxable_income = max(0, gross_income - total_deductions)
        
        # Calculate tax based on slabs (FY 2024-25)
        if taxable_income <= 300000:
            tax = 0
        elif taxable_income <= 700000:
            tax = (taxable_income - 300000) * 0.05
        elif taxable_income <= 1000000:
            tax = 20000 + (taxable_income - 700000) * 0.20
        elif taxable_income <= 1700000:
            tax = 80000 + (taxable_income - 1000000) * 0.30
        else:
            tax = 290000 + (taxable_income - 1700000) * 0.45
        
        # Add cess
        cess = tax * 0.04
        total_tax = tax + cess
        
        return round(total_tax, 2)
    
    def _calculate_new_regime_tax(self, gross_income: float) -> float:
        """Calculate tax under new regime (no deductions)"""
        
        # New regime tax slabs (FY 2024-25)
        if gross_income <= 300000:
            tax = 0
        elif gross_income <= 700000:
            tax = (gross_income - 300000) * 0.05
        elif gross_income <= 1000000:
            tax = 20000 + (gross_income - 700000) * 0.10
        elif gross_income <= 1700000:
            tax = 50000 + (gross_income - 1000000) * 0.15
        elif gross_income <= 2500000:
            tax = 155000 + (gross_income - 1700000) * 0.20
        else:
            tax = 315000 + (gross_income - 2500000) * 0.30
        
        # Add cess
        cess = tax * 0.04
        total_tax = tax + cess
        
        return round(total_tax, 2)
    
    def _identify_missed_deductions(self, financial_data: Dict) -> List[Dict]:
        """Identify common missed deductions"""
        
        missed = []
        
        # 80C Deductions (max ₹1.5 lakh)
        current_80c = financial_data.get("sip_annual", 0) + financial_data.get("insurance_premium", 0)
        if current_80c < 150000:
            missed.append({
                "deduction": "Section 80C",
                "current": current_80c,
                "max_available": 150000,
                "gap": 150000 - current_80c,
                "suggestion": f"Increase SIP contributions by ₹{150000 - current_80c} or buy insurance policies"
            })
        
        # 80D Health Insurance
        if financial_data.get("health_insurance", 0) == 0:
            missed.append({
                "deduction": "Section 80D",
                "current": 0,
                "max_available": 100000,
                "gap": 100000,
                "suggestion": "Buy health insurance for self and family - excellent coverage benefit"
            })
        
        # 80E Education Loan Interest
        if financial_data.get("education_loan_interest", 0) == 0:
            missed.append({
                "deduction": "Section 80E",
                "current": 0,
                "max_available": 50000,
                "gap": 50000,
                "suggestion": "If you have education loan, claim interest as deduction (no limit)"
            })
        
        return missed
    
    def _optimize_hra(self, financial_data: Dict) -> Dict:
        """Optimize HRA claims"""
        
        hra_amount = financial_data.get("hra_received", 0)
        annual_income = financial_data.get("annual_income", 0)
        rent_paid = financial_data.get("rent_paid", 0)
        city = financial_data.get("city", "Non-metro")
        
        # HRA exemption is min of: (a) HRA received, (b) 50% of salary (metro) or 40% (non-metro), (c) rent - 10% of salary
        metro_cities = ["Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata"]
        percentage = 0.50 if city in metro_cities else 0.40
        
        max_hra = min(
            hra_amount,
            annual_income * percentage,
            max(0, rent_paid - (annual_income * 0.10))
        )
        
        return {
            "hra_received": hra_amount,
            "hra_exemption": round(max_hra, 2),
            "taxable_hra": round(hra_amount - max_hra, 2),
            "optimization_tip": "Keep rent receipts. HRA is fully exempted if conditions are met."
        }
    
    def _recommend_nps(self, financial_data: Dict) -> Dict:
        """Recommend NPS contributions for tax saving + retirement"""
        
        annual_income = financial_data.get("annual_income", 0)
        age = financial_data.get("age", 30)
        existing_nps = financial_data.get("existing_nps_contribution", 0)
        
        # NPS limits
        section_80c_nps_limit = 150000
        section_80ccd1b_limit = 50000  # Additional limit for salaried
        total_nps_limit = section_80c_nps_limit + section_80ccd1b_limit
        
        # Recommended contribution (15% of income for retirement)
        recommended = min(total_nps_limit, annual_income * 0.15)
        gap = recommended - existing_nps
        
        expected_return = 0.08 + (1 if age < 40 else 0)  # Higher expected return for younger age
        years_to_retirement = 60 - age
        
        if gap > 0:
            corpus_at_retirement = existing_nps * ((1 + expected_return) ** years_to_retirement)
            corpus_with_nps = (existing_nps + gap) * ((1 + expected_return) ** years_to_retirement)
        else:
            corpus_at_retirement = existing_nps * ((1 + expected_return) ** years_to_retirement)
            corpus_with_nps = corpus_at_retirement
        
        return {
            "current_annual_contribution": existing_nps,
            "recommended_annual_contribution": round(recommended, 2),
            "additional_investment_needed": round(gap, 2),
            "expected_corpus_at_retirement": round(corpus_with_nps, 2),
            "tax_benefit_annual": round(gap * 0.30, 2),  # 30% tax slab assumption
            "tip": "NPS gives both tax deduction and retirement corpus - win-win investment"
        }
    
    def _get_optimization_suggestions(self, financial_data, old_tax, new_tax, missed_deductions):
        """Get AI-powered tax optimization suggestions"""
        
        prompt = f"""
        Tax optimization analysis for a user:
        - Gross Income: ₹{financial_data.get('annual_income')}
        - Age: {financial_data.get('age')}
        - Tax under Old Regime: ₹{old_tax}
        - Tax under New Regime: ₹{new_tax}
        - Missed Deductions: {json.dumps(missed_deductions)}
        
        Provide 3-4 specific, prioritized tax optimization suggestions.
        Focus on: 80C maximization, HRA optimization, NPS, health insurance, education loan interest.
        Format as a concise list with potential tax savings.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error getting suggestions: {e}")
            return [
                "Maximize Section 80C investments (SIP + Insurance)",
                "Take health insurance if not already covered",
                "Consider NPS for retirement + tax savings",
                "Choose regime that minimizes your tax based on your income structure"
            ]
