"""Модуль авиакомпании-перевозчика."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Airline:
    """Авиакомпания, осуществляющая перевозки."""

    def __init__(self, name: str, iata_code: str) -> None:
        """Инициализирует экземпляр класса Airline."""
        self.name = name
        self.iata_code = iata_code
        self._fleet: list[Aircraft] = []

    @property
    def fleet_size(self) -> int:
        """Текущее количество самолетов во флоте компании."""
        return len(self._fleet)

    @property
    def fleet(self) -> list[Aircraft]:
        """Возвращает значение атрибута fleet."""
        return list(self._fleet)

    def register_aircraft(self, aircraft: Aircraft) -> None:
        """Регистрирует воздушное судно в парке авиакомпании."""
        if aircraft not in self._fleet:
            self._fleet.append(aircraft)

    def remove_aircraft(self, aircraft: Aircraft) -> None:
        """Выводит воздушное судно из летного парка авиакомпании."""
        if aircraft in self._fleet:
            self._fleet.remove(aircraft)

    def get_fleet(self) -> list[Aircraft]:
        """Возвращает копию списка флота для безопасного перебора."""
        return list(self._fleet)

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Airline(name={self.name!r}, iata={self.iata_code!r}, fleet={len(self._fleet)})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Airline):
            return NotImplemented
        return self.iata_code == other.iata_code

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.iata_code)
