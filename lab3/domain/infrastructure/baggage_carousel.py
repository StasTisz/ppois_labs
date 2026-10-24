"""Модуль транспортерной ленты выдачи багажа."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class BaggageCarousel:
    """Багажная карусель для выдачи чемоданов по прилету."""

    def __init__(self, number: int) -> None:
        """Инициализирует экземпляр класса BaggageCarousel."""
        self.number = number
        self._is_active = False
        self._assigned_flight: Flight | None = None

    @property
    def is_active(self) -> bool:
        """Возвращает признак active."""
        return self._is_active

    @property
    def assigned_flight(self) -> Flight | None:
        """Возвращает значение атрибута assigned_flight."""
        return self._assigned_flight

    def activate(self, flight: Flight | None = None) -> None:
        """Привязывает карусель к рейсу и запускает конвейер."""
        self._assigned_flight = flight
        self._is_active = True

    def deactivate(self) -> None:
        """Останавливает конвейер после выдачи всего багажа."""
        self._is_active = False
        self._assigned_flight = None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"BaggageCarousel(number={self.number}, active={self._is_active})"
