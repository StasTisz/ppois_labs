from datetime import UTC, datetime

import pytest

from lab3.domain.exceptions import InvalidTicketException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_ticket():
    p = Passenger("П", "П", "P-2")
    plane = PassengerAircraft("P", 800.0, "RA-TKT", 1000.0, 100)
    flight = DepartureFlight(
        "B2-900", Airline("A", "A"), plane, FlightPlan("O", "D", datetime.now(UTC))
    )
    t = Ticket(p, flight, "Business", 350.0, ticket_number="TKT-001")
    assert t.passenger == p
    assert t.flight_number == "B2-900"
    assert t.flight == flight
    assert t.is_used is False
    assert t.seat_class == "Business"
    assert t.price == 350.0
    assert "Ticket" in repr(t)
    assert t == Ticket(p, flight, "Business", 350.0, ticket_number="TKT-001")
    assert t != "NotATicket"

    t.upgrade_class("First", additional_fee=150.0)
    assert t.seat_class == "First"
    assert t.price == 500.0

    t2 = Ticket(p, flight, "Economy", 100.0)
    t2.cancel_ticket()
    assert t2.price == 0.0

    t.use_ticket()
    assert t.is_used is True

    with pytest.raises(InvalidTicketException):
        t.use_ticket()

    with pytest.raises(InvalidTicketException):
        t.cancel_ticket()

    with pytest.raises(InvalidTicketException):
        t.upgrade_class("Suite")
