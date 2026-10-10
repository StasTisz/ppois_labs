from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.aircraft import Aircraft


class CargoAircraft(Aircraft):
    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, max_payload_kg: float
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_payload_kg = max_payload_kg
        self._current_payload_kg = 0.0
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = False

    @property
    def current_payload_kg(self) -> float:
        return self._current_payload_kg

    def load_cargo(self, weight: float) -> None:
        if self._current_payload_kg + weight > self.max_payload_kg:
            raise CapacityExceededException("Перевес: превышена максимальная грузоподъемность.")
        self._current_payload_kg += weight

    def unload_cargo(self) -> float:
        weight = self._current_payload_kg
        self._current_payload_kg = 0.0
        return weight

    def perform_maintenance(self) -> None:
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
