"""Модуль взлетно-посадочной полосы (ВПП) аэродрома."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import RunwayBusyException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Runway:
    """Взлетно-посадочная полоса.
    Отвечает за координацию занятости при взлетах и посадках."""

    def __init__(self, number: str, length: int) -> None:
        """Инициализирует экземпляр класса Runway."""
        self.number = number
        self.length = length
        self._is_busy = False
        self._current_aircraft: Aircraft | None = None

    @property
    def is_busy(self) -> bool:
        """Возвращает признак busy."""
        return self._is_busy

    @property
    def current_aircraft(self) -> Aircraft | None:
        """Возвращает значение атрибута current_aircraft."""
        return self._current_aircraft

    def occupy(self, aircraft: Aircraft) -> None:
        """Занимает полосу указанным воздушным судном."""
        if self._is_busy:
            raise RunwayBusyException(f"Полоса {self.number} уже занята.")
        self._is_busy = True
        self._current_aircraft = aircraft

    def clear(self) -> None:
        """Освобождает полосу после завершения взлета или руления на перрон."""
        self._is_busy = False
        self._current_aircraft = None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Runway(number={self.number!r}, length={self.length}, busy={self._is_busy})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Runway):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.number)
