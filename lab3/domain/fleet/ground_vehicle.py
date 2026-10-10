from __future__ import annotations

from abc import ABC

from lab3.domain.fleet.vehicle import Vehicle


class GroundVehicle(Vehicle, ABC):
    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed)
        self.license_plate = license_plate
        self.is_available = True

    def dispatch(self) -> None:
        if not self.is_available:
            raise ValueError(f"Техника {self.license_plate} уже занята.")
        self.is_available = False

    def release(self) -> None:
        self.is_available = True
