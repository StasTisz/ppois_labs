"""Модуль грузового транспортного самолета."""

from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.aircraft import Aircraft


class CargoAircraft(Aircraft):
    """Грузовой самолет. Оперирует весом груза и механизмами рампы."""

    def __init__(
        self,
        model: str,
        max_speed: float,
        tail_number: str,
        fuel_capacity: float,
        max_payload_kg: float,
    ) -> None:
        """Инициализирует экземпляр класса CargoAircraft."""
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_payload_kg = max_payload_kg
        self._current_payload_kg = 0.0
        self.cargo_hydraulics_ok = False
        self.winch_mechanism_inspected = False

    @property
    def current_payload_kg(self) -> float:
        """Текущий вес загруженного груза в килограммах (доступно только для чтения)."""
        return self._current_payload_kg

    def load_cargo(self, weight_kg: float) -> None:
        """Загружает карго с проверкой максимальной грузоподъемности."""
        if weight_kg <= 0:
            raise ValueError("Вес груза должен быть положительным.")
        if self._current_payload_kg + weight_kg > self.max_payload_kg:
            raise CapacityExceededException(
                f"Превышена грузоподъемность: {self.max_payload_kg} кг."
            )
        self._current_payload_kg += weight_kg

    def unload_cargo(self) -> float:
        """Полностью выгружает карго-трюм."""
        unloaded = self._current_payload_kg
        self._current_payload_kg = 0.0
        return unloaded

    def perform_maintenance(self) -> None:
        """ТО грузового борта: диагностика гидравлики рампы и лебедки."""
        self.cargo_hydraulics_ok = True
        self.winch_mechanism_inspected = True
        self.requires_maintenance = False
