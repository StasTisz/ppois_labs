from datetime import UTC, datetime
from lab3.domain.operations.flight_plan import FlightPlan


def test_flight_plan():
    now = datetime.now(UTC)
    plan = FlightPlan("MSQ", "DXB", now)
    assert plan.origin == "MSQ"
    assert plan.destination == "DXB"
    assert plan.scheduled_time == now
    assert "MSQ-DXB-CORRIDOR-1" in plan.air_corridor
