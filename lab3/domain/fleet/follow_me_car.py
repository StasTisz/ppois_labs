from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class FollowMeCar(GroundVehicle):
    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed, license_plate)
        self.lightbar_tested = False

    def lead_aircraft(self, aircraft: Aircraft, destination: str) -> str:
        self.dispatch()
        result = f"Борт {aircraft.tail_number} успешно сопровожден к: {destination}"
        self.release()
        return result

    def perform_maintenance(self) -> None:
        self.lightbar_tested = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
