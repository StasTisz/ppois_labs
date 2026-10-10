from __future__ import annotations

import uuid

from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
from lab3.domain.infrastructure.check_in_counter import CheckInCounter
from lab3.domain.infrastructure.gate import Gate
from lab3.domain.infrastructure.lounge import Lounge


class Terminal:
    def __init__(self, name: str) -> None:
        self.terminal_id = str(uuid.uuid4())
        self.name = name
        self._gates: list[Gate] = []
        self._check_in_counters: list[CheckInCounter] = []
        self._carousels: list[BaggageCarousel] = []
        self._lounges: list[Lounge] = []

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
