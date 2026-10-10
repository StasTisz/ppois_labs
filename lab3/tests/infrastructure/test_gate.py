from datetime import UTC, datetime
import pytest
from lab3.domain.exceptions import GateNotAssignedException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan


def test_gate():
    gate = Gate("B04")
    assert gate.is_open is False

    with pytest.raises(GateNotAssignedException):
        gate.open_gate()

    plane = PassengerAircraft("P", 800.0, "RA-G", 1000.0, 100)
    flight1 = DepartureFlight("B2-10", Airline("A1", "A1"), plane, FlightPlan("O", "D", datetime.now(UTC)))
    flight2 = DepartureFlight("B2-20", Airline("A2", "A2"), plane, FlightPlan("O", "D", datetime.now(UTC)))

    gate.assign_flight(flight1)
    assert gate.current_flight == flight1

    with pytest.raises(ValueError):
        gate.assign_flight(flight2)

    gate.open_gate()
    assert gate.is_open is True

    gate.clear_gate()
    assert gate.is_open is False
    assert gate.current_flight is None
