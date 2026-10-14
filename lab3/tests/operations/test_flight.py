from datetime import UTC, datetime

import pytest

from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.infrastructure.runway import Runway
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.flight import Flight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.people.pilot import Pilot


class DummyFlight(Flight):
    pass


def test_flight_base():
    plane = PassengerAircraft("P", 800.0, "RA-F", 1000.0, 100)
    airline = Airline("A", "A")
    plan = FlightPlan("O", "D", datetime.now(UTC))
    f = DummyFlight("A-1", airline, plane, plan)

    assert f.status == "Scheduled"
    assert "DummyFlight" in repr(f)
    assert f == DummyFlight("A-1", airline, plane, plan)
    assert f != "NotAFlight"
    assert len({f, DummyFlight("A-1", airline, plane, plan)}) == 1

    # Crew
    pilot = Pilot("Иван", "И", "P-11", 2000.0, "ATPL")
    f.assign_crew(pilot)
    assert len(f.crew) == 1
    crew_copy = f.crew
    crew_copy.clear()
    assert len(f.crew) == 1

    # Gate & Runway
    gate = Gate("G-10")
    f.assign_gate(gate)
    assert f.gate == gate

    runway = Runway("09L", 3000)
    f.assign_runway(runway)
    assert f.runway == runway

    # Passengers collection
    pass_copy = f.passengers
    pass_copy.clear()
    assert len(f.passengers) == 0

    f.delay("Late arrival")
    assert f.status == "Delayed"
    assert f.delay_reason == "Late arrival"

    f.cancel()
    assert f.status == "Cancelled"

    with pytest.raises(ValueError):
        f.delay("Weather")
