from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.infrastructure.check_in_counter import CheckInCounter
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.infrastructure.lounge import Lounge
from lab3.domain.infrastructure.terminal import Terminal


def test_terminal():
    term = Terminal("Terminal 1")
    gate = Gate("A01")
    counter = CheckInCounter(1)
    car = BaggageCarousel(1)
    lounge = Lounge("VIP", 20)

    term.add_gate(gate)
    term.add_counter(counter)
    term.add_carousel(car)
    term.add_lounge(lounge)

    assert term.get_gate("A01") == gate
    assert term.get_gate("Z99") is None
