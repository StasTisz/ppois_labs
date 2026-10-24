from datetime import UTC, datetime

import pytest

from lab3.domain.exceptions import (
    BoardingClosedException,
    FlightDelayedException,
    GateNotAssignedException,
    InvalidTicketException,
    MaintenanceRequiredException,
    NoAvailableCrewException,
)
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger
from lab3.domain.people.pilot import Pilot


def test_departure_flight():
    plane = PassengerAircraft("P", 800.0, "RA-DF", 1000.0, 100)
    flight = DepartureFlight(
        "B2-10", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC))
    )

    # Test GateNotAssignedException
    with pytest.raises(GateNotAssignedException):
        flight.start_boarding()

    gate = Gate("G-1")
    flight.assign_gate(gate)

    p = Passenger("П", "П", "P-10")
    flight_other = DepartureFlight(
        "XX-99", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC))
    )
    t_valid = Ticket(p, flight, "Economy", 100.0)
    t_other = Ticket(p, flight_other, "Economy", 100.0)

    with pytest.raises(InvalidTicketException):
        flight.check_in_passenger(p, t_other)

    bp = flight.check_in_passenger(p, t_valid)
    assert bp.ticket == t_valid
    assert len(flight.manifest) == 1

    bag = Baggage(12.0, p)
    flight.load_baggage(bag)
    assert len(flight.cargo_hold) == 1

    # Before boarding started
    with pytest.raises(BoardingClosedException):
        flight.board_passenger(p, bp)

    flight.start_boarding()
    assert flight.status == "Boarding"
    assert gate.is_open is True

    # Board passenger successfully
    flight.board_passenger(p, bp)
    assert bp.is_boarded is True

    flight.close_boarding()
    assert flight.status == "BoardingClosed"
    assert gate.is_open is False

    with pytest.raises(BoardingClosedException):
        flight.board_passenger(p, bp)

    # Authorize takeoff checks
    with pytest.raises(NoAvailableCrewException):
        flight.authorize_takeoff()

    pilot = Pilot("Капитан", "К", "PIL-01", 3000.0, "ATPL", is_captain=True)
    flight.assign_crew(pilot)

    plane.requires_maintenance = True
    with pytest.raises(MaintenanceRequiredException):
        flight.authorize_takeoff()

    plane.requires_maintenance = False
    assert flight.authorize_takeoff() is True

    flight.cancel()
    with pytest.raises(FlightDelayedException):
        flight.check_in_passenger(p, t_valid)
