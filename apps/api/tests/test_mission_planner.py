from app.services.mission_planner import build_mission, classify_intent


def test_grocery_request_becomes_a_plan_without_claiming_checkout() -> None:
    mission = build_mission("Order 2 litres milk from Blinkit")

    assert mission is not None
    assert mission.intent == "grocery"
    assert mission.state == "not_executable"
    assert any(step.action_class == "irreversible" for step in mission.steps)
    assert "not connected" in mission.steps[1].description.lower()


def test_flight_request_asks_for_route_and_date() -> None:
    mission = build_mission("Find me a flight")

    assert mission is not None
    assert mission.intent == "flight_search"
    assert "Departure city and destination" in mission.missing_information
    assert "Travel date" in mission.missing_information
    assert mission.state == "needs_input"


def test_flight_request_with_required_details_still_does_not_claim_live_search() -> None:
    mission = build_mission("Find a flight from Bhopal to Delhi tomorrow")

    assert mission is not None
    assert mission.missing_information == []
    assert mission.state == "not_executable"
    assert all(step.state != "ready" or step.action_class == "none" for step in mission.steps)


def test_hinglish_grocery_keywords_route_to_grocery_planner() -> None:
    assert classify_intent("Blinkit se doodh aur sabzi mangwana hai") == "grocery"


def test_general_conversation_does_not_create_a_mission() -> None:
    assert build_mission("Hey Warik, how are you?") is None


def test_trip_prompt_creates_an_itinerary_mission() -> None:
    mission = build_mission("Plan a trip from Bhopal to Goa next weekend")

    assert mission is not None
    assert mission.intent == "travel_planning"
    assert mission.missing_information == []
    assert mission.state == "not_executable"
    assert any(step.title == "Build the day-by-day plan" for step in mission.steps)
