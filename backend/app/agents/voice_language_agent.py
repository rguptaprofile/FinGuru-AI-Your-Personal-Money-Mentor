from __future__ import annotations

from app.agents.advisor_agent import answer_financial_query
from app.models.schemas import AdvisorV2Input, AdvisorV2Response, ChatInput


def _to_hindi_mode_text(text: str) -> str:
    # Phase-2 scaffold only; wire a translation provider for production use.
    return f"Hindi Mode: {text}"


def answer_query_with_language_voice(payload: AdvisorV2Input) -> AdvisorV2Response:
    base = answer_financial_query(ChatInput(question=payload.question, profile=payload.profile))
    answer_text = _to_hindi_mode_text(base.answer) if payload.language == "hi" else base.answer

    tts_text = answer_text if payload.voice_enabled else None
    tts_provider_hint = "Integrate Azure Speech or gTTS in production" if payload.voice_enabled else None

    return AdvisorV2Response(
        answer_text=answer_text,
        language=payload.language,
        tts_text=tts_text,
        tts_provider_hint=tts_provider_hint,
        disclaimer=base.disclaimer,
    )