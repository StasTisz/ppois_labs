from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.check_in_agent import CheckInAgent


class CheckInCounter:
    def __init__(self, number: int) -> None:
        self.number = number
        self._is_open = False
        self._current_agent: CheckInAgent | None = None
        self._assigned_flight: Flight | None = None
        self._accepted_baggage: list[Baggage] = []

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def current_agent(self) -> CheckInAgent | None:
        return self._current_agent

    @property
    def assigned_flight(self) -> Flight | None:
        return self._assigned_flight

    @property
    def accepted_baggage(self) -> list[Baggage]:
        return list(self._accepted_baggage)

    def open_counter(self, agent: CheckInAgent, flight: Flight) -> None:
        self._current_agent = agent
        self._assigned_flight = flight
        self._is_open = True

    def close_counter(self) -> None:
        self._is_open = False
        self._current_agent = None
        self._assigned_flight = None
        self._accepted_baggage.clear()

    def accept_baggage(self, baggage: Baggage) -> None:
        if not self._is_open:
            raise ValueError("Стойка регистрации закрыта.")
        self._accepted_baggage.append(baggage)

    def __repr__(self) -> str:
        return f"CheckInCounter(number={self.number}, open={self._is_open})"
