from __future__ import annotations

import uuid

from lab3.domain.exceptions import CapacityExceededException


class ParkingLot:
    def __init__(self, name: str, capacity: int) -> None:
        self.lot_id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self._parked_cars: set[str] = set()

    def park_car(self, license_plate: str) -> None:
        if len(self._parked_cars) >= self.capacity:
            raise CapacityExceededException(f"Парковка '{self.name}' переполнена.")
        self._parked_cars.add(license_plate)

    def remove_car(self, license_plate: str) -> None:
        self._parked_cars.discard(license_plate)
