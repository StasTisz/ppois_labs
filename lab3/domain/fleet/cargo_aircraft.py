from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.aircraft import Aircraft


class CargoAircraft(Aircraft):
    def __init__(
        self,
        model: str,
        max_speed: float,
        tail_number: str,
        fuel_capacity: float,
        max_payload_kg: float,
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_payload_kg = max_payload_kg
        self._current_payload_kg = 0.0
        self.cargo_hydraulics_ok = False
        self.winch_mechanism_inspected = False

    @property
    def current_payload_kg(self) -> float:
        return self._current_payload_kg

    def load_cargo(self, weight_kg: float) -> None:
        if weight_kg <= 0:
            raise ValueError("Вес груза должен быть положительным.")
        if self._current_payload_kg + weight_kg > self.max_payload_kg:
            raise CapacityExceededException(
                f"Превышена грузоподъемность: {self.max_payload_kg} кг."
            )
        self._current_payload_kg += weight_kg

    def unload_cargo(self) -> float:
        unloaded = self._current_payload_kg
        self._current_payload_kg = 0.0
        return unloaded

    def perform_maintenance(self) -> None:
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = True
        self.requires_maintenance = False
