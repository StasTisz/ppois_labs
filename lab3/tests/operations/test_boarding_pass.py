from datetime import UTC, datetime

import pytest

from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.boarding_pass import BoardingPass
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_boarding_pass():
    p = Passenger("П", "П", "P-3")
    plane = PassengerAircraft("P", 800.0, "RA-BP", 1000.0, 100)
    flight = DepartureFlight(
        "B2-901", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC))
    )
    t = Ticket(p, flight, "Economy", 120.0)
    gate = Gate("A03")

    bp1 = BoardingPass(t, "14B", gate)
    assert bp1.ticket == t
    assert bp1.seat_number == "14B"
    assert bp1.gate == gate
    assert bp1.gate_number == "A03"
    assert bp1.is_boarded is False
    assert bp1.verify_gate(gate) is True
    assert bp1.verify_gate(Gate("B01")) is False
    assert "BoardingPass" in repr(bp1)
    assert "Seat 14B" in bp1.get_summary()

    bp1.change_seat("14A")
    assert bp1.seat_number == "14A"

    bp1.mark_boarded()
    assert bp1.is_boarded is True

    with pytest.raises(ValueError, match="посадка уже завершена"):
        bp1.change_seat("15A")

    bp2 = BoardingPass(t, "14C", None)
    assert bp2.gate is None
    assert bp2.gate_number == "TBD"
    assert bp2.verify_gate(gate) is False

    bp2.assign_gate(gate)
    assert bp2.gate == gate
    assert bp2.gate_number == "A03"
