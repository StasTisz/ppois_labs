from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle


class PassengerBus(GroundVehicle):
    def __init__(self, model: str, max_speed: float, license_plate: str, capacity: int) -> None:
        super().__init__(model, max_speed, license_plate)
        self.capacity = capacity
        self._passengers_count = 0
        self.doors_pneumatics_checked = False

    @property
    def passengers_count(self) -> int:
        return self._passengers_count

    def board(self, count: int) -> None:
        if self._passengers_count + count > self.capacity:
            raise CapacityExceededException("Перронный автобус переполнен.")
        self._passengers_count += count

    def drop_off(self) -> int:
        count = self._passengers_count
        self._passengers_count = 0
        return count

    def perform_maintenance(self) -> None:
        self.doors_pneumatics_checked = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
