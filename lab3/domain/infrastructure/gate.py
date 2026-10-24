"""Модуль выхода на посадку (гейта) пассажирского терминала."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import GateNotAssignedException

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class Gate:
    """Выход на посадку (гейт) в терминале.
    Связывает инфраструктуру терминала с конкретным авиарейсом."""

    def __init__(self, number: str) -> None:
        """Инициализирует экземпляр класса Gate."""
        self.number = number
        self._is_open = False
        self._current_flight: Flight | None = None

    @property
    def is_open(self) -> bool:
        """Возвращает признак open."""
        return self._is_open

    @property
    def current_flight(self) -> Flight | None:
        """Возвращает значение атрибута current_flight."""
        return self._current_flight

    def assign_flight(self, flight: Flight) -> None:
        """Привязывает рейс к гейту для подготовки к посадке."""
        if self._current_flight is not None and self._current_flight != flight:
            raise ValueError(f"Гейт {self.number} уже обслуживает другой рейс.")
        self._current_flight = flight

    def open_gate(self) -> None:
        """Открывает двери гейта для посадки по талонам."""
        if self._current_flight is None:
            raise GateNotAssignedException(
                f"Нельзя открыть гейт {self.number}: рейс не назначен."
            )
        self._is_open = True

    def close_gate(self) -> None:
        """Останавливает пропуск пассажиров на рейс."""
        self._is_open = False

    def clear_gate(self) -> None:
        """Полностью освобождает гейт после отбытия судна."""
        self.close_gate()
        self._current_flight = None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        flight_str = getattr(self._current_flight, "flight_number", "None")
        return (
            f"Gate(number={self.number!r}, open={self._is_open}, flight={flight_str!r})"
        )

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Gate):
            return NotImplemented
        return self.number == other.number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.number)
