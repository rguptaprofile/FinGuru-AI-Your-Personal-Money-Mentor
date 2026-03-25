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
