from __future__ import annotations

from openai import OpenAI

from app.config import settings
from app.models.schemas import ChatInput, ChatResponse


def _fallback_answer(question: str) -> str:
    question_lower = question.lower()
    if "sip" in question_lower:
        return "Start with a SIP equal to at least 20% of your monthly income and increase it 10% yearly."
    if "tax" in question_lower:
        return "Compare old vs new regime yearly and use 80C, 80D, and NPS deductions to reduce tax burden."
    if "emergency" in question_lower:
        return "Maintain an emergency corpus of 6 months of essential expenses in liquid funds or savings account."
    return "Focus on budgeting, emergency fund, insurance, and disciplined monthly SIP investing for long-term wealth."


def answer_financial_query(payload: ChatInput) -> ChatResponse:
    disclaimer = "Educational guidance only. This is not a SEBI-registered investment advisory service."

    if not settings.openai_api_key:
        return ChatResponse(answer=_fallback_answer(payload.question), disclaimer=disclaimer)

    client = OpenAI(api_key=settings.openai_api_key)
    system_prompt = (
        "You are FinGuru AI, an India-focused personal finance mentor. "
        "Give practical, concise, and safe guidance. Mention assumptions and avoid guarantees."
    )
    user_prompt = f"Question: {payload.question}\nProfile: {payload.profile.model_dump() if payload.profile else 'Not provided'}"

    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_output_tokens=300,
    )

    answer = response.output_text.strip() if response.output_text else _fallback_answer(payload.question)
    return ChatResponse(answer=answer, disclaimer=disclaimer)
