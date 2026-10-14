from __future__ import annotations

from abc import ABC

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.vehicle import Vehicle


class Aircraft(Vehicle, ABC):
    def __init__(
        self, model: str, max_speed: float, tail_number: str, fuel_capacity: float
    ) -> None:
        super().__init__(model, max_speed)
        self.tail_number = tail_number
        self.fuel_capacity = fuel_capacity
        self._current_fuel = 0.0
        self.is_in_flight = False
        self.is_cleaned = True

    @property
    def current_fuel(self) -> float:
        return self._current_fuel

    def refuel(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Объем заправки должен быть положительным.")
        if self._current_fuel + amount > self.fuel_capacity:
            raise CapacityExceededException(
                f"Баки переполнены. Максимум: {self.fuel_capacity} л."
            )
        self._current_fuel = round(self._current_fuel + amount, 2)

    def clean(self) -> None:
        self.is_cleaned = True

    def take_off(self) -> None:
        self.is_in_flight = True

    def land(self) -> None:
        self.is_in_flight = False
        self.requires_maintenance = True
        self.is_cleaned = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tail={self.tail_number!r}, model={self.model!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.tail_number == other.tail_number

    def __hash__(self) -> int:
        return hash(self.tail_number)
