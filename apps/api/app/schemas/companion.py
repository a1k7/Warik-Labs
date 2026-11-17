from typing import Literal

from pydantic import BaseModel, Field, field_validator


class ConversationTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=3000)


class CompanionChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    history: list[ConversationTurn] = Field(default_factory=list, max_length=12)

    @field_validator("message")
    @classmethod
    def strip_message(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Message cannot be blank.")
        return value


class MissionStep(BaseModel):
    id: str
    title: str
    description: str
    state: Literal["ready", "needs_input", "blocked"]
    action_class: Literal["read_only", "reversible", "irreversible", "none"] = "none"


class MissionPlan(BaseModel):
    id: str
    title: str
    objective: str
    intent: str
    state: Literal["draft", "needs_input", "waiting_approval", "not_executable"]
    steps: list[MissionStep]
    missing_information: list[str] = Field(default_factory=list)
    capabilities_used: list[str] = Field(default_factory=list)
    execution_note: str


class CompanionChatResponse(BaseModel):
    reply: str
    provider: Literal["groq", "local"]
    provider_status: Literal["connected", "fallback", "not_configured"]
    mission: MissionPlan | None = None
    suggested_prompts: list[str] = Field(default_factory=list)
    safety_note: str
