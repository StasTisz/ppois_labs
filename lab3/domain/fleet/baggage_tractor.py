from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle


class BaggageTractor(GroundVehicle):
    def __init__(self, model: str, max_speed: float, license_plate: str, max_carts: int = 4) -> None:
        super().__init__(model, max_speed, license_plate)
        self.max_carts = max_carts
        self._current_carts = 0
        self.tow_hitch_greased = False

    @property
    def current_carts(self) -> int:
        return self._current_carts

    def attach_cart(self) -> None:
        if self._current_carts >= self.max_carts:
            raise CapacityExceededException("Достигнут лимит багажных тележек.")
        self._current_carts += 1

    def detach_all_carts(self) -> None:
        self._current_carts = 0

    def perform_maintenance(self) -> None:
        self.tow_hitch_greased = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
