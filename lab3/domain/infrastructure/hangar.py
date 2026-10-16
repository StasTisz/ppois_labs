"""Модуль авиаремонтного ангара для стоянки и техобслуживания."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Hangar:
    """Технический ангар для длительной стоянки и ремонта воздушных судов."""

    def __init__(self, number: int, capacity: int = 5) -> None:
        """Инициализирует экземпляр класса Hangar."""
        self.number = number
        self.capacity = capacity
        self._stored_aircraft: list[Aircraft] = []

    @property
    def current_occupancy(self) -> int:
        """Возвращает значение атрибута current_occupancy."""
        return len(self._stored_aircraft)

    @property
    def stored_aircraft(self) -> list[Aircraft]:
        """Возвращает значение атрибута stored_aircraft."""
        return list(self._stored_aircraft)

    def store_aircraft(self, aircraft: Aircraft) -> None:
        """Отправляет борт в ангар с проверкой наличия мест."""
        if len(self._stored_aircraft) >= self.capacity:
            raise CapacityExceededException(
                f"Ангар #{self.number} полон (максимум {self.capacity} ВС)."
            )
        if aircraft not in self._stored_aircraft:
            self._stored_aircraft.append(aircraft)

    def release_aircraft(self, aircraft: Aircraft) -> None:
        """Выпускает борт из ангара на перрон."""
        if aircraft in self._stored_aircraft:
            self._stored_aircraft.remove(aircraft)

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Hangar(number={self.number}, stored={len(self._stored_aircraft)}/{self.capacity})"
