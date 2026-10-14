from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class FollowMeCar(GroundVehicle):
    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed, license_plate)
        self.flashing_lights_active = False
        self.lightbar_tested = False

    def toggle_lights(self) -> None:
        self.flashing_lights_active = not self.flashing_lights_active

    def lead_aircraft(self, aircraft: Aircraft, target_stand: str) -> str:
        self.flashing_lights_active = True
        return f"Машина сопровождения {self.license_plate} ведет борт {aircraft.tail_number} на стоянку {target_stand}."

    def perform_maintenance(self) -> None:
        self.lightbar_tested = True
        self.requires_maintenance = False
