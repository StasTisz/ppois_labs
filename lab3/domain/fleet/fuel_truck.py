from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class FuelTruck(GroundVehicle):
    def __init__(self, model: str, max_speed: float, license_plate: str, tank_capacity: float) -> None:
        super().__init__(model, max_speed, license_plate)
        self.tank_capacity = tank_capacity
        self._current_fuel = tank_capacity
        self.pump_calibrated = False
        self.filter_replaced = False

    @property
    def current_fuel(self) -> float:
        return self._current_fuel

    def refuel_aircraft(self, aircraft: Aircraft, amount: float) -> None:
        if self._current_fuel < amount:
            raise CapacityExceededException("В цистерне топливозаправщика недостаточно керосина.")
        self.dispatch()
        aircraft.refuel(amount)
        self._current_fuel -= amount
        self.release()

    def perform_maintenance(self) -> None:
        self.pump_calibrated = True
        self.filter_replaced = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
