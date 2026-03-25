from fastapi import APIRouter

from app.agents.advisor_agent import answer_financial_query
from app.agents.goal_planning_agent import build_fire_roadmap
from app.agents.money_health_agent import evaluate_money_health
from app.agents.tax_optimizer_agent import compare_tax_regimes
from app.agents.voice_language_agent import answer_query_with_language_voice
from app.models.schemas import (
    AdvisorV2Input,
    AdvisorV2Response,
    ChatInput,
    ChatResponse,
    MoneyHealthResponse,
    PlannerResponse,
    ProfileInput,
    TaxInput,
    TaxResponse,
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
