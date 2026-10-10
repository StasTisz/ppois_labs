from datetime import UTC, datetime
import pytest
from lab3.domain.exceptions import FlightDelayedException, InvalidTicketException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_departure_flight():
    plane = PassengerAircraft("P", 800.0, "RA-DF", 1000.0, 100)
    flight = DepartureFlight("B2-10", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC)))
    gate = Gate("G-1")
    flight.assign_gate(gate)

    p = Passenger("П", "П", "P-10")
    t_valid = Ticket(p, "B2-10", "Economy", 100.0)
    t_other = Ticket(p, "XX-99", "Economy", 100.0)

    with pytest.raises(InvalidTicketException):
        flight.check_in_passenger(p, t_other)

    bp = flight.check_in_passenger(p, t_valid)
    assert bp.ticket == t_valid
    assert len(flight.manifest) == 1

    bag = Baggage(12.0, p)
    flight.load_baggage(bag)
    assert len(flight.cargo_hold) == 1

    flight.start_boarding()
    assert flight.status == "Boarding"
    assert gate.is_open is True

    flight.cancel()
    with pytest.raises(FlightDelayedException):
        flight.check_in_passenger(p, t_valid)
