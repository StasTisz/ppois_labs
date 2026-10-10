from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_passenger():
    p = Passenger("Пётр", "Петров", "MP7654321")
    assert p.has_tickets is False
    assert p.baggage_count == 0

    t = Ticket(p, "B2-101", "Economy", 150.0)
    p.buy_ticket(t)
    assert p.has_tickets is True
    assert len(p.get_tickets()) == 1

    b = Baggage(15.0, p)
    p.add_baggage(b)
    assert p.baggage_count == 1
