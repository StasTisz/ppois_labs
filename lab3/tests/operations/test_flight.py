from datetime import UTC, datetime
import pytest
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.flight import Flight
from lab3.domain.operations.flight_plan import FlightPlan


class DummyFlight(Flight):
    pass


def test_flight_base():
    plane = PassengerAircraft("P", 800.0, "RA-F", 1000.0, 100)
    airline = Airline("A", "A")
    plan = FlightPlan("O", "D", datetime.now(UTC))
    f = DummyFlight("A-1", airline, plane, plan)

    assert f.status == "Scheduled"
    f.delay("Late arrival")
    assert f.status == "Delayed"
    assert f.delay_reason == "Late arrival"

    f.cancel()
    assert f.status == "Cancelled"

    with pytest.raises(ValueError):
        f.delay("Weather")
