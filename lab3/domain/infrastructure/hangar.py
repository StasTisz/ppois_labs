from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Hangar:
    def __init__(self, number: str, capacity: int) -> None:
        self.hangar_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self._aircrafts: list[Aircraft] = []

    def store_aircraft(self, aircraft: Aircraft) -> None:
        if len(self._aircrafts) >= self.capacity:
            raise CapacityExceededException(f"Ангар {self.number} заполнен.")
        self._aircrafts.append(aircraft)

    def release_aircraft(self, aircraft: Aircraft) -> None:
        if aircraft in self._aircrafts:
            self._aircrafts.remove(aircraft)
