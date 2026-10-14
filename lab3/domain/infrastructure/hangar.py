from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Hangar:
    def __init__(self, number: int, capacity: int = 5) -> None:
        self.number = number
        self.capacity = capacity
        self._stored_aircraft: list[Aircraft] = []

    @property
    def current_occupancy(self) -> int:
        return len(self._stored_aircraft)

    @property
    def stored_aircraft(self) -> list[Aircraft]:
        return list(self._stored_aircraft)

    def store_aircraft(self, aircraft: Aircraft) -> None:
        if len(self._stored_aircraft) >= self.capacity:
            raise CapacityExceededException(
                f"Ангар #{self.number} полон (максимум {self.capacity} ВС)."
            )
        if aircraft not in self._stored_aircraft:
            self._stored_aircraft.append(aircraft)

    def release_aircraft(self, aircraft: Aircraft) -> None:
        if aircraft in self._stored_aircraft:
            self._stored_aircraft.remove(aircraft)

    def __repr__(self) -> str:
        return f"Hangar(number={self.number}, stored={len(self._stored_aircraft)}/{self.capacity})"
