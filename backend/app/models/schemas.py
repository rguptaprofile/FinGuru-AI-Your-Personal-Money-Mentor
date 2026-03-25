from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class GoalInput(BaseModel):
    name: str = Field(..., description="Goal label, e.g., Retirement")
    target_amount: float = Field(..., gt=0)
    years_to_goal: int = Field(..., ge=1, le=50)
    priority: Literal["high", "medium", "low"] = "medium"


class ProfileInput(BaseModel):
    age: int = Field(..., ge=18, le=75)
    monthly_income: float = Field(..., gt=0)
    monthly_expenses: float = Field(..., ge=0)
    monthly_emi: float = Field(0, ge=0)
    existing_investments: float = Field(0, ge=0)
    emergency_fund: float = Field(0, ge=0)
    annual_insurance_cover: float = Field(0, ge=0)
    annual_salary: float = Field(..., ge=0)
    risk_appetite: Literal["conservative", "balanced", "aggressive"] = "balanced"
    goals: list[GoalInput] = Field(default_factory=list)


class MoneyHealthDimension(BaseModel):
    name: str
    score: int = Field(..., ge=0, le=100)
    insight: str


class MoneyHealthResponse(BaseModel):
    total_score: int
    status: str
    dimensions: list[MoneyHealthDimension]
    recommendations: list[str]


class SIPPlanItem(BaseModel):
    goal_name: str
    monthly_sip: float
    expected_corpus: float
    years_to_goal: int


class AssetAllocation(BaseModel):
    equity: int
    debt: int
    gold: int
    cash: int


class PlannerResponse(BaseModel):
    total_monthly_sip: float
    asset_allocation: AssetAllocation
    emergency_fund_target: float
    insurance_gap: float
    monthly_roadmap: list[str]
    goals: list[SIPPlanItem]


class TaxInput(BaseModel):
    annual_salary: float = Field(..., ge=0)
    section_80c: float = Field(0, ge=0)
    section_80d: float = Field(0, ge=0)
    hra_exemption: float = Field(0, ge=0)
    home_loan_interest: float = Field(0, ge=0)
    other_deductions: float = Field(0, ge=0)


class TaxRegimeResult(BaseModel):
    taxable_income: float
    tax_before_cess: float
    cess: float
    total_tax: float


class TaxResponse(BaseModel):
    old_regime: TaxRegimeResult
    new_regime: TaxRegimeResult
    better_regime: Literal["old", "new", "same"]
    tax_saved: float
    suggestions: list[str]


class ChatInput(BaseModel):
    question: str = Field(..., min_length=3, max_length=1500)
    profile: ProfileInput | None = None


class ChatResponse(BaseModel):
    answer: str
    disclaimer: str


class AdvisorV2Input(BaseModel):
    question: str = Field(..., min_length=3, max_length=1500)
    language: Literal["en", "hi"] = "en"
    voice_enabled: bool = False
    profile: ProfileInput | None = None


class AdvisorV2Response(BaseModel):
    answer_text: str
    language: Literal["en", "hi"]
    tts_text: str | None = None
    tts_provider_hint: str | None = None
    disclaimer: str


class LifeEventInput(BaseModel):
    event_type: Literal["bonus", "inheritance", "marriage", "new_baby", "job_change"]
    amount: float = Field(0, ge=0)
    profile: ProfileInput


class LifeEventResponse(BaseModel):
    event_type: str
    action_plan: list[str]
    suggested_allocation: dict[str, float]


class CouplePartnerInput(BaseModel):
    name: str
    annual_salary: float = Field(..., ge=0)
    section_80c: float = Field(0, ge=0)
    section_80d: float = Field(0, ge=0)
    monthly_expenses: float = Field(..., ge=0)
    monthly_emi: float = Field(0, ge=0)


class CouplesPlannerInput(BaseModel):
    partner_one: CouplePartnerInput
    partner_two: CouplePartnerInput
    annual_rent_paid: float = Field(0, ge=0)
    combined_goal_sip_target: float = Field(0, ge=0)


class CouplesPlannerResponse(BaseModel):
    combined_annual_income: float
    combined_monthly_surplus: float
    suggested_sip_split: dict[str, float]
    tax_optimization_notes: list[str]


class TaxWizardInput(BaseModel):
    annual_salary: float = Field(..., ge=0)
    has_form16_text: str | None = None
    section_80c: float = Field(0, ge=0)
    section_80d: float = Field(0, ge=0)
    hra_exemption: float = Field(0, ge=0)
    home_loan_interest: float = Field(0, ge=0)
    other_deductions: float = Field(0, ge=0)


class TaxWizardResponse(BaseModel):
    missing_deductions: list[str]
    old_vs_new_summary: TaxResponse
    ranked_tax_saving_options: list[str]


class MFPortfolioInput(BaseModel):
    statement_source: Literal["cams", "kfintech", "manual"] = "manual"
    invested_amount: float = Field(..., gt=0)
    current_value: float = Field(..., gt=0)
    years_held: float = Field(..., gt=0)
    expense_ratio_percent: float = Field(1.2, ge=0, le=5)
    benchmark_return_percent: float = Field(12, ge=0, le=30)


class MFPortfolioResponse(BaseModel):
    estimated_xirr_percent: float
    benchmark_comparison_percent: float
    expense_drag_amount: float
    overlap_risk_level: Literal["low", "medium", "high"]
    rebalance_plan: list[str]
