import pytest
from lab3.domain.exceptions import InvalidTicketException
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_ticket():
    p = Passenger("П", "П", "P-2")
    t = Ticket(p, "B2-900", "Business", 350.0)
    assert t.passenger == p
    assert t.flight_number == "B2-900"
    assert t.is_used is False

    t.use_ticket()
    assert t.is_used is True

    with pytest.raises(InvalidTicketException):
        t.use_ticket()
