"""Модуль базового воздушного судна авиапарка."""

from __future__ import annotations

from abc import ABC

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.vehicle import Vehicle


class Aircraft(Vehicle, ABC):
    """Абстрактный класс воздушного судна.
    Отвечает за базовые механики полета и заправки."""

    def __init__(
        self, model: str, max_speed: float, tail_number: str, fuel_capacity: float
    ) -> None:
        """Инициализирует экземпляр класса Aircraft."""
        super().__init__(model, max_speed)
        self.tail_number = tail_number
        self.fuel_capacity = fuel_capacity
        self._current_fuel = 0.0
        self.is_in_flight = False
        self.is_cleaned = True

    @property
    def current_fuel(self) -> float:
        """Текущий уровень топлива в баках (доступно только для чтения)."""
        return self._current_fuel

    def refuel(self, amount: float) -> None:
        """Заправляет самолет указанным объемом топлива."""
        if amount <= 0:
            raise ValueError("Объем заправки должен быть положительным.")
        if self._current_fuel + amount > self.fuel_capacity:
            raise CapacityExceededException(
                f"Баки переполнены. Максимум: {self.fuel_capacity} л."
            )
        self._current_fuel = round(self._current_fuel + amount, 2)

    def clean(self) -> None:
        """Проводит влажную уборку и дезинфекцию пассажирского салона воздушного судна."""
        self.is_cleaned = True

    def take_off(self) -> None:
        """Переводит борт в статус полета."""
        self.is_in_flight = True

    def land(self) -> None:
        """Регистрирует приземление борта.
        После каждого рейса автоматически выставляется флаг необходимости ТО."""
        self.is_in_flight = False
        self.requires_maintenance = True
        self.is_cleaned = False

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"{self.__class__.__name__}(tail={self.tail_number!r}, model={self.model!r})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Aircraft):
            return NotImplemented
        return self.tail_number == other.tail_number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.tail_number)
