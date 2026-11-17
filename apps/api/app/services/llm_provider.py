import httpx

from app.config import settings
from app.schemas.companion import ConversationTurn

SYSTEM_PROMPT = """You are Warik, an India-first personal AI companion.
Be warm, sharp, practical and proactive. Understand English, Hinglish and Indian context.
Help the user make progress: identify the real goal, constraints, missing information and a sensible next step.
Be concise but thoughtful. Do not overuse bullet points.
Never claim that you searched a live provider, booked, ordered, paid, sent a message, changed a calendar,
or accessed a website unless a connected tool explicitly returned evidence. No such external-action tools
are available in this release. You may draft, reason, plan and ask clarifying questions.
Never ask for passwords, OTPs, API keys, card numbers or raw credentials.
For financial, purchase, booking or messaging requests, state that you can prepare the plan but cannot
execute the external side effect in this build. Never ask the user to paste secrets into chat.
"""


async def generate_reply(
    message: str, history: list[ConversationTurn]
) -> str | None:
    if not settings.groq_api_key or not settings.groq_api_key.get_secret_value():
        return None

    api_key = settings.groq_api_key.get_secret_value()
    model = settings.groq_model
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(
        {"role": turn.role, "content": turn.content[-3000:]} for turn in history[-8:]
    )
    messages.append({"role": "user", "content": message})

    async with httpx.AsyncClient(timeout=httpx.Timeout(25.0, connect=8.0)) as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.35,
                "max_tokens": 700,
            },
        )
        response.raise_for_status()
        payload = response.json()

    content = payload.get("choices", [{}])[0].get("message", {}).get("content")
    if isinstance(content, str) and content.strip():
        return content.strip()
    return None
