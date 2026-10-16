"""Модуль аэродромного топливозаправщика."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class FuelTruck(GroundVehicle):
    """Автомобиль-топливозаправщик. Перекачивает топливо в баки судов."""

    def __init__(
        self,
        model: str,
        max_speed: float,
        license_plate: str,
        tank_capacity: float,
    ) -> None:
        """Инициализирует экземпляр класса FuelTruck."""
        super().__init__(model, max_speed, license_plate)
        self.tank_capacity = tank_capacity
        self._current_fuel = tank_capacity
        self.pump_calibrated = False
        self.filter_replaced = False

    def perform_maintenance(self) -> None:
        """ТО заправщика: регламентная замена фильтров и калибровка счетчика."""
        self.pump_calibrated = True
        self.filter_replaced = True
        self.requires_maintenance = False

    @property
    def current_fuel(self) -> float:
        """Текущий остаток топлива в цистерне заправщика."""
        return self._current_fuel

    def refuel_aircraft(self, aircraft: Aircraft, amount: float) -> None:
        """Перекачивает керосин из цистерны грузовика в баки самолета."""
        if amount <= 0:
            raise ValueError("Объем перекачки топлива должен быть положительным.")
        if amount > self._current_fuel:
            raise CapacityExceededException(
                f"В заправщике {self.license_plate} недостаточно топлива ({self._current_fuel} л.)."
            )
        aircraft.refuel(amount)
        self._current_fuel = round(self._current_fuel - amount, 2)

    def replenish_tank(self, amount: float) -> None:
        """Пополняет цистерну топливозаправщика авиационным керосином."""
        if amount <= 0:
            raise ValueError("Объем пополнения должен быть положительным.")
        if self._current_fuel + amount > self.tank_capacity:
            raise CapacityExceededException(
                f"Цистерна заправщика {self.license_plate} переполнена (макс {self.tank_capacity} л.)."
            )
        self._current_fuel = round(self._current_fuel + amount, 2)
