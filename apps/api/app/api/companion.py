import logging

import httpx
from fastapi import APIRouter

from app.config import settings
from app.schemas.companion import CompanionChatRequest, CompanionChatResponse
from app.services.llm_provider import generate_reply
from app.services.mission_planner import build_mission, local_reply

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/companion", tags=["companion"])


@router.post("/chat", response_model=CompanionChatResponse)
async def chat(request: CompanionChatRequest) -> CompanionChatResponse:
    mission = build_mission(request.message)
    provider = "local"
    provider_status = "not_configured"
    reply = None

    if settings.groq_api_key and settings.groq_api_key.get_secret_value():
        try:
            reply = await generate_reply(request.message, request.history)
            if reply:
                provider = "groq"
                provider_status = "connected"
        except (httpx.HTTPError, ValueError, KeyError, IndexError):
            logger.warning("Groq companion request failed; using local response.")
            provider_status = "fallback"

    if not reply:
        reply = local_reply(request.message, mission)
        if provider_status == "not_configured":
            provider_status = "not_configured"
        else:
            provider_status = "fallback"

    prompts = (
        ["Plan my day around these deadlines", "Help me organise a trip", "Remind me to follow up tomorrow"]
        if mission is None
        else ["Make this plan more specific", "What information do you still need?", "Show me safer alternatives"]
    )

    return CompanionChatResponse(
        reply=reply,
        provider=provider,
        provider_status=provider_status,
        mission=mission,
        suggested_prompts=prompts,
        safety_note="Planning only · No external action was executed",
    )
