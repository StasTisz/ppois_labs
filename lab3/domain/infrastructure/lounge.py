from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class Lounge:
    def __init__(self, name: str, capacity: int, is_vip: bool = False) -> None:
        self.lounge_id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self.is_vip = is_vip
        self._passengers: list[Passenger] = []

    def enter(self, passenger: Passenger) -> None:
        if len(self._passengers) >= self.capacity:
            raise CapacityExceededException(f"Зал {self.name} переполнен.")
        self._passengers.append(passenger)

    def exit(self, passenger: Passenger) -> None:
        if passenger in self._passengers:
            self._passengers.remove(passenger)

    @property
    def current_occupancy(self) -> int:
        return len(self._passengers)
