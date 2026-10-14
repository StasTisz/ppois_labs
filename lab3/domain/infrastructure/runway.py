from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import RunwayBusyException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Runway:
    def __init__(self, number: str, length: int) -> None:
        self.number = number
        self.length = length
        self._is_busy = False
        self._current_aircraft: Aircraft | None = None

    @property
    def is_busy(self) -> bool:
        return self._is_busy

    @property
    def current_aircraft(self) -> Aircraft | None:
        return self._current_aircraft

    def occupy(self, aircraft: Aircraft) -> None:
        if self._is_busy:
            raise RunwayBusyException(f"Полоса {self.number} уже занята.")
        self._is_busy = True
        self._current_aircraft = aircraft

    def clear(self) -> None:
        self._is_busy = False
        self._current_aircraft = None

    def __repr__(self) -> str:
        return f"Runway(number={self.number!r}, length={self.length}, busy={self._is_busy})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Runway):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        return hash(self.number)
