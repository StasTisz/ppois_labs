import pytest

from lab3.domain.exceptions import InvalidTicketException
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_ticket():
    p = Passenger("П", "П", "P-2")
    t = Ticket(p, "B2-900", "Business", 350.0, ticket_number="TKT-001")
    assert t.passenger == p
    assert t.flight_number == "B2-900"
    assert t.is_used is False
    assert t.passenger_id == "P-2"
    assert t.seat_class == "Business"
    assert t.price == 350.0
    assert "Ticket" in repr(t)
    assert t == Ticket(p, "B2-900", "Business", 350.0, ticket_number="TKT-001")
    assert t != "NotATicket"

    t.upgrade_class("First", additional_fee=150.0)
    assert t.seat_class == "First"
    assert t.price == 500.0

    t2 = Ticket(p, "B2-900", "Economy", 100.0)
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
