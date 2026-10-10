from lab3.domain.infrastructure.gate import Gate
from lab3.domain.operations.boarding_pass import BoardingPass
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.passenger import Passenger


def test_boarding_pass():
    p = Passenger("П", "П", "P-3")
    t = Ticket(p, "B2-901", "Economy", 120.0)
    gate = Gate("A03")

    bp1 = BoardingPass(t, "14B", gate)
    assert bp1.ticket == t
    assert bp1.seat_number == "14B"
    assert bp1.gate == gate
    assert bp1.gate_number == "A03"

    bp2 = BoardingPass(t, "14C", "TBD")
    assert bp2.gate is None
    assert bp2.gate_number == "TBD"
