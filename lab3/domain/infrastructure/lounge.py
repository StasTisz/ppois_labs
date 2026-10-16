"""Модуль зала ожидания повышенной комфортности (Lounge)."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class Lounge:
    """Зал ожидания для пассажиров (бизнес-залы, VIP-комнаты)."""

    def __init__(self, name: str, capacity: int = 50, is_vip: bool = False) -> None:
        """Инициализирует экземпляр класса Lounge."""
        self.name = name
        self.capacity = capacity
        self.is_vip = is_vip
        self._guests: list[Passenger] = []

    @property
    def current_occupancy(self) -> int:
        """Возвращает значение атрибута current_occupancy."""
        return len(self._guests)

    @property
    def free_seats(self) -> int:
        """Возвращает значение атрибута free_seats."""
        return self.capacity - len(self._guests)

    @property
    def guests(self) -> list[Passenger]:
        """Возвращает значение атрибута guests."""
        return list(self._guests)

    def enter(self, passenger: Passenger) -> None:
        """Впускает пассажира с проверкой лимита вместимости."""
        if len(self._guests) >= self.capacity:
            raise CapacityExceededException(
                f"Бизнес-зал '{self.name}' переполнен (максимум {self.capacity} гостей)."
            )
        if passenger not in self._guests:
            self._guests.append(passenger)

    def exit(self, passenger: Passenger) -> None:
        """Регистрирует выход пассажира из зала."""
        if passenger in self._guests:
            self._guests.remove(passenger)

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return (
            f"Lounge(name={self.name!r}, occupancy={len(self._guests)}/{self.capacity})"
        )
