from __future__ import annotations

from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.infrastructure.check_in_counter import CheckInCounter
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.infrastructure.lounge import Lounge


class Terminal:
    def __init__(self, name: str) -> None:
        self.name = name
        self._gates: list[Gate] = []
        self._check_in_counters: list[CheckInCounter] = []
        self._carousels: list[BaggageCarousel] = []
        self._lounges: list[Lounge] = []

    @property
    def gates(self) -> list[Gate]:
        return list(self._gates)

    @property
    def check_in_counters(self) -> list[CheckInCounter]:
        return list(self._check_in_counters)

    @property
    def carousels(self) -> list[BaggageCarousel]:
        return list(self._carousels)

    @property
    def lounges(self) -> list[Lounge]:
        return list(self._lounges)

    def add_gate(self, gate: Gate) -> None:
        self._gates.append(gate)

    def add_counter(self, counter: CheckInCounter) -> None:
        self._check_in_counters.append(counter)

    def add_carousel(self, carousel: BaggageCarousel) -> None:
        self._carousels.append(carousel)

    def add_lounge(self, lounge: Lounge) -> None:
        self._lounges.append(lounge)

    def get_gate(self, number: str) -> Gate | None:
        for gate in self._gates:
            if gate.number == number:
                return gate
        return None

    def __repr__(self) -> str:
        return f"Terminal(name={self.name!r}, gates={len(self._gates)}, counters={len(self._check_in_counters)})"
