from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.check_in_agent import CheckInAgent


class CheckInCounter:
    def __init__(self, number: int) -> None:
        self.counter_id = str(uuid.uuid4())
        self.number = number
        self.is_open = False
        self.current_agent: CheckInAgent | None = None
        self.assigned_flight: Flight | None = None
        self._accepted_baggage: list[Baggage] = []

    def open_counter(self, agent: CheckInAgent, flight: Flight) -> None:
        self.current_agent = agent
        self.assigned_flight = flight
        self.is_open = True

    def close_counter(self) -> None:
        self.is_open = False
        self.current_agent = None
        self.assigned_flight = None
        self._accepted_baggage.clear()

    def accept_baggage(self, baggage: Baggage) -> None:
        if not self.is_open:
            raise ValueError("Стойка регистрации закрыта.")
        self._accepted_baggage.append(baggage)
