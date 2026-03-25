from fastapi import APIRouter

from app.agents.advisor_agent import answer_financial_query
from app.agents.couples_planner_agent import build_couples_plan
from app.agents.goal_planning_agent import build_fire_roadmap
from app.agents.life_event_agent import advise_on_life_event
from app.agents.mf_xray_agent import analyze_mf_portfolio
from app.agents.money_health_agent import evaluate_money_health
from app.agents.tax_optimizer_agent import compare_tax_regimes
from app.agents.tax_wizard_agent import run_tax_wizard
from app.agents.voice_language_agent import answer_query_with_language_voice
from app.models.schemas import (
    AdvisorV2Input,
    AdvisorV2Response,
    ChatInput,
    ChatResponse,
    CouplesPlannerInput,
    CouplesPlannerResponse,
    LifeEventInput,
    LifeEventResponse,
    MFPortfolioInput,
    MFPortfolioResponse,
    MoneyHealthResponse,
    PlannerResponse,
    ProfileInput,
    TaxInput,
    TaxResponse,
    TaxWizardInput,
    TaxWizardResponse,
)

router = APIRouter(prefix="/finance", tags=["finance"])


@router.post("/money-health", response_model=MoneyHealthResponse)
def money_health(payload: ProfileInput) -> MoneyHealthResponse:
    return evaluate_money_health(payload)


@router.post("/fire-planner", response_model=PlannerResponse)
def fire_planner(payload: ProfileInput) -> PlannerResponse:
    return build_fire_roadmap(payload)


@router.post("/tax-optimizer", response_model=TaxResponse)
def tax_optimizer(payload: TaxInput) -> TaxResponse:
    return compare_tax_regimes(payload)


@router.post("/advisor-chat", response_model=ChatResponse)
def advisor_chat(payload: ChatInput) -> ChatResponse:
    return answer_financial_query(payload)


@router.post("/advisor-chat-v2", response_model=AdvisorV2Response)
def advisor_chat_v2(payload: AdvisorV2Input) -> AdvisorV2Response:
    return answer_query_with_language_voice(payload)


@router.post("/life-event-advisor", response_model=LifeEventResponse)
def life_event_advisor(payload: LifeEventInput) -> LifeEventResponse:
    return advise_on_life_event(payload)


@router.post("/couples-planner", response_model=CouplesPlannerResponse)
def couples_planner(payload: CouplesPlannerInput) -> CouplesPlannerResponse:
    return build_couples_plan(payload)


@router.post("/tax-wizard", response_model=TaxWizardResponse)
def tax_wizard(payload: TaxWizardInput) -> TaxWizardResponse:
    return run_tax_wizard(payload)


@router.post("/mf-portfolio-xray", response_model=MFPortfolioResponse)
def mf_portfolio_xray(payload: MFPortfolioInput) -> MFPortfolioResponse:
    return analyze_mf_portfolio(payload)
