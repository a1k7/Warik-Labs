import re
import uuid

from app.schemas.companion import MissionPlan, MissionStep

DATE_HINTS = (
    r"\b(?:today|tomorrow|tonight|kal|aaj|parso|this weekend|next weekend|next week|on monday|on tuesday|on wednesday|"
    r"on thursday|on friday|on saturday|on sunday)\b",
    r"\b\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?\b",
)
ACTION_WORDS = re.compile(
    r"\b(order|buy|book|pay|send|submit|cancel|reserve|purchase|recharge|transfer)\b",
    re.I,
)


def _has(text: str, *terms: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in terms)


def _extract_missing(text: str, intent: str) -> list[str]:
    missing: list[str] = []
    has_date = any(re.search(pattern, text, re.I) for pattern in DATE_HINTS)
    if intent == "flight_search":
        if not re.search(r"\bfrom\s+.+?\s+to\s+|\bto\s+.+?\s+from\s+", text, re.I):
            missing.append("Departure city and destination")
        if not has_date:
            missing.append("Travel date")
    elif intent == "cab":
        if not _has(text, "from ") or not _has(text, "to "):
            missing.append("Pickup and drop-off locations")
    elif intent == "travel_planning":
        if not re.search(r"\bfrom\s+.+?\s+to\s+", text, re.I):
            missing.append("Starting city and destination")
        if not has_date:
            missing.append("Travel dates or duration")
    elif intent in {"grocery", "food"}:
        if not _has(text, "order ", "get me ", "buy ", "add ") and intent == "grocery":
            missing.append("Items and quantities")
    elif intent == "reminder" and not has_date:
        missing.append("Reminder date or time")
    return missing


def classify_intent(text: str) -> str:
    if _has(text, "flight", "air ticket", "fly to", "airfare"):
        return "flight_search"
    if _has(text, "plan a trip", "plan my trip", "travel plan", "itinerary", "holiday", "vacation", "trip from", "travel to"):
        return "travel_planning"
    if _has(text, "blinkit", "instamart", "bigbasket", "grocery", "groceries", "milk", "vegetables"):
        return "grocery"
    if _has(text, "swiggy", "zomato", "food order", "restaurant order", "dinner order"):
        return "food"
    if _has(text, "ola", "uber", "cab", "taxi", "ride"):
        return "cab"
    if _has(text, "remind me", "reminder", "don't let me forget", "follow up", "follow-up"):
        return "reminder"
    if _has(text, "plan my day", "schedule my day", "organise my day", "organize my day"):
        return "daily_plan"
    if _has(text, "research", "compare", "find information", "look up"):
        return "research"
    if ACTION_WORDS.search(text):
        return "external_action"
    return "conversation"


def build_mission(text: str) -> MissionPlan | None:
    intent = classify_intent(text)
    if intent == "conversation":
        return None

    missing = _extract_missing(text, intent)
    titles = {
        "flight_search": "Find the right flight",
        "travel_planning": "Plan your trip",
        "grocery": "Prepare your grocery order",
        "food": "Find food options",
        "cab": "Plan your cab ride",
        "reminder": "Create a reminder",
        "daily_plan": "Organise your day",
        "research": "Research and compare",
        "external_action": "Review requested action",
    }
    objective = text.strip()
    step_specs: list[tuple[str, str, str, str]] = []

    if intent == "flight_search":
        step_specs = [
            ("Understand route", "Extract origin, destination, date and travel constraints.", "ready", "none"),
            ("Check flight options", "Live fare search is not connected in this build.", "blocked", "read_only"),
            ("Compare options", "Compare schedule, total price and baggage once results are available.", "blocked", "read_only"),
        ]
    elif intent == "travel_planning":
        step_specs = [
            ("Shape the itinerary", "Organise destination, dates, trip pace and budget.", "needs_input" if missing else "ready", "none"),
            ("Research transport and stays", "Live flight and hotel inventory is not connected in this build.", "blocked", "read_only"),
            ("Build the day-by-day plan", "Prepare a practical itinerary once the trip constraints are confirmed.", "ready", "none"),
        ]
    elif intent == "grocery":
        step_specs = [
            ("Confirm basket", "Structure the requested items, quantities and substitutions.", "needs_input" if missing else "ready", "none"),
            ("Check store availability", "Blinkit/Instamart/BigBasket is not connected yet.", "blocked", "read_only"),
            ("Review checkout", "Any purchase would require a separate explicit approval.", "blocked", "irreversible"),
        ]
    elif intent == "food":
        step_specs = [
            ("Understand the meal", "Capture cuisine, dietary preferences, budget and delivery location.", "ready", "none"),
            ("Find restaurants", "Live menus and delivery inventory are not connected yet.", "blocked", "read_only"),
            ("Review order", "No order will be placed without an approved integration and explicit approval.", "blocked", "irreversible"),
        ]
    elif intent == "cab":
        step_specs = [
            ("Confirm journey", "Capture pickup, drop-off and pickup time.", "needs_input" if missing else "ready", "none"),
            ("Compare ride options", "Live Ola/Uber fares and vehicle availability are not connected.", "blocked", "read_only"),
            ("Confirm booking", "A ride booking would require explicit approval.", "blocked", "irreversible"),
        ]
    elif intent == "reminder":
        step_specs = [
            ("Confirm reminder", "Extract the reminder and due time.", "needs_input" if missing else "ready", "none"),
            ("Schedule notification", "A notification scheduler is not connected in this build.", "blocked", "reversible"),
        ]
    elif intent == "daily_plan":
        step_specs = [
            ("Collect commitments", "Identify tasks, deadlines and available time.", "ready", "none"),
            ("Prioritise the day", "Group work by urgency, impact and estimated effort.", "ready", "none"),
            ("Review schedule", "Proposed schedule only; nothing is added to a calendar.", "ready", "none"),
        ]
    elif intent == "research":
        step_specs = [
            ("Clarify the question", "Define scope, decision criteria and freshness needs.", "ready", "none"),
            ("Gather evidence", "Live web research is not enabled in this local demo.", "blocked", "read_only"),
            ("Synthesis", "Produce a comparison when sources are available.", "blocked", "none"),
        ]
    else:
        step_specs = [
            ("Clarify the outcome", "Identify the target account, object and exact requested change.", "needs_input", "none"),
            ("Review consequences", "External actions are disabled until integrations and approvals are implemented.", "blocked", "irreversible"),
        ]

    steps = [
        MissionStep(
            id=f"step-{index + 1}",
            title=title,
            description=description,
            state=state,  # type: ignore[arg-type]
            action_class=action_class,  # type: ignore[arg-type]
        )
        for index, (title, description, state, action_class) in enumerate(step_specs)
    ]

    if missing:
        state = "needs_input"
    elif any(step.state == "blocked" for step in steps):
        state = "not_executable"
    else:
        state = "draft"

    return MissionPlan(
        id=str(uuid.uuid4()),
        title=titles.get(intent, "New mission"),
        objective=objective,
        intent=intent,
        state=state,  # type: ignore[arg-type]
        steps=steps,
        missing_information=missing,
        execution_note="Planning only. No external website, merchant, calendar, message or payment was accessed.",
    )


def local_reply(text: str, mission: MissionPlan | None) -> str:
    if mission is None:
        return (
            "I'm here. Tell me what you're trying to get done, what constraints matter, "
            "and what a good outcome looks like. I'll turn it into a clear plan and keep "
            "the difference between a suggestion, an attempted action and a verified result visible."
        )

    if mission.missing_information:
        return (
            f"I've started a plan for {mission.title.lower()}. Before I can make it useful, "
            f"I need: {', '.join(mission.missing_information)}. Share those details and I'll refine the plan. "
            "I won't place an order, make a booking or spend money."
        )

    if mission.intent == "travel_planning":
        return (
            f"I've shaped this into {mission.title.lower()}. I can organise the itinerary, budget and trip priorities. "
            "Live fares and hotel availability are not connected yet, so I won't invent quotes or claim anything is booked."
        )

    if mission.intent in {"daily_plan", "reminder"}:
        return (
            f"I've structured this as {mission.title.lower()}. We can work through the details here. "
            "This build can draft and organise the plan, but it does not yet send notifications or change your calendar."
        )

    return (
        f"I've turned that into a mission: {mission.title}. The plan is prepared, but the required live "
        "provider connection is not available yet. I can help refine the requirements and prepare the next step; "
        "I won't claim a search, order or booking has happened."
    )
