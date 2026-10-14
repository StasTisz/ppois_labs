from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class BaggageCarousel:
    def __init__(self, number: int) -> None:
        self.number = number
        self._is_active = False
        self._assigned_flight: Flight | None = None

    @property
    def is_active(self) -> bool:
        return self._is_active

    @property
    def assigned_flight(self) -> Flight | None:
        return self._assigned_flight

    def activate(self, flight: Flight | None = None) -> None:
        self._assigned_flight = flight
        self._is_active = True

    def deactivate(self) -> None:
        self._is_active = False
        self._assigned_flight = None

    def __repr__(self) -> str:
        return f"BaggageCarousel(number={self.number}, active={self._is_active})"
