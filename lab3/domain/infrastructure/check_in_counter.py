"""Модуль стойки регистрации пассажиров и багажа в терминале."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.check_in_agent import CheckInAgent


class CheckInCounter:
    """Стойка регистрации пассажиров и приема багажа."""

    def __init__(self, number: int) -> None:
        """Инициализирует экземпляр класса CheckInCounter."""
        self.number = number
        self._is_open = False
        self._current_agent: CheckInAgent | None = None
        self._assigned_flight: Flight | None = None
        self._accepted_baggage: list[Baggage] = []

    @property
    def is_open(self) -> bool:
        """Возвращает признак open."""
        return self._is_open

    @property
    def current_agent(self) -> CheckInAgent | None:
        """Возвращает значение атрибута current_agent."""
        return self._current_agent

    @property
    def assigned_flight(self) -> Flight | None:
        """Возвращает значение атрибута assigned_flight."""
        return self._assigned_flight

    @property
    def accepted_baggage(self) -> list[Baggage]:
        """Возвращает значение атрибута accepted_baggage."""
        return list(self._accepted_baggage)

    def open_counter(self, agent: CheckInAgent, flight: Flight) -> None:
        """Открывает смену на стойке регистрации."""
        self._current_agent = agent
        self._assigned_flight = flight
        self._is_open = True

    def close_counter(self) -> None:
        """Закрывает стойку и отправляет принятый багаж в систему сортировки."""
        self._is_open = False
        self._current_agent = None
        self._assigned_flight = None
        self._accepted_baggage.clear()

    def accept_baggage(self, baggage: Baggage) -> None:
        """Принимает единицу багажа на конвейерную ленту."""
        if not self._is_open:
            raise ValueError("Стойка регистрации закрыта.")
        self._accepted_baggage.append(baggage)

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"CheckInCounter(number={self.number}, open={self._is_open})"
