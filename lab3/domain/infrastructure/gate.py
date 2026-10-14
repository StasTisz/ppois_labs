from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import GateNotAssignedException

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class Gate:
    def __init__(self, number: str) -> None:
        self.number = number
        self._is_open = False
        self._current_flight: Flight | None = None

    @property
    def is_open(self) -> bool:
        return self._is_open

    @property
    def current_flight(self) -> Flight | None:
        return self._current_flight

    def assign_flight(self, flight: Flight) -> None:
        if self._current_flight is not None and self._current_flight != flight:
            raise ValueError(f"Гейт {self.number} уже обслуживает другой рейс.")
        self._current_flight = flight

    def open_gate(self) -> None:
        if self._current_flight is None:
            raise GateNotAssignedException(
                f"Нельзя открыть гейт {self.number}: рейс не назначен."
            )
        self._is_open = True

    def close_gate(self) -> None:
        self._is_open = False

    def clear_gate(self) -> None:
        self.close_gate()
        self._current_flight = None

    def __repr__(self) -> str:
        flight_str = getattr(self._current_flight, "flight_number", "None")
        return (
            f"Gate(number={self.number!r}, open={self._is_open}, flight={flight_str!r})"
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Gate):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        return hash(self.number)
