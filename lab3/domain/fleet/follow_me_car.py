"""Модуль аэродромного автомобиля сопровождения (Follow-Me)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class FollowMeCar(GroundVehicle):
    """Машина сопровождения эскорта (Follow Me Car)."""

    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        """Инициализирует экземпляр класса FollowMeCar."""
        super().__init__(model, max_speed, license_plate)
        self.flashing_lights_active = False
        self.lightbar_tested = False

    def toggle_lights(self) -> None:
        """Переключает проблесковые светосигнальные огни автомобиля сопровождения."""
        self.flashing_lights_active = not self.flashing_lights_active

    def lead_aircraft(self, aircraft: Aircraft, target_stand: str) -> str:
        """Сопровождает самолет до заданной точки (гейта или ВПП)."""
        self.flashing_lights_active = True
        return f"Машина сопровождения {self.license_plate} ведет борт {aircraft.tail_number} на стоянку {target_stand}."

    def perform_maintenance(self) -> None:
        """ТО машины эскорта: тест светодиодного табло и радиостанции."""
        self.lightbar_tested = True
        self.requires_maintenance = False
