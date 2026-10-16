"""Модуль плана полета воздушного судна."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from datetime import datetime


class FlightPlan:
    """Маршрутный лист и расписание конкретного рейса."""

    INTERNATIONAL_DURATION_HOURS: float = 2.5
    DOMESTIC_DURATION_HOURS: float = 1.0

    def __init__(
        self,
        origin: str,
        destination: str,
        scheduled_time: datetime,
        air_corridor: str | None = None,
        flight_level: int = 350,
    ) -> None:
        """Инициализирует экземпляр класса FlightPlan."""
        self.origin = origin
        self.destination = destination
        self.scheduled_time = scheduled_time
        self.air_corridor = air_corridor or f"{origin}-{destination}-CORRIDOR-1"
        self.flight_level = flight_level

    def calculate_flight_duration_hours(self) -> float:
        # Условная стандартная оценка длительности межсекторного полета
        """Рассчитывает плановую продолжительность перелета в часах."""
        return (
            self.INTERNATIONAL_DURATION_HOURS
            if self.is_international()
            else self.DOMESTIC_DURATION_HOURS
        )

    def change_destination(self, new_destination: str) -> None:
        """Изменяет аэропорт назначения в плане полета."""
        if not new_destination.strip():
            raise ValueError("Пункт назначения не может быть пустым.")
        self.destination = new_destination

    def is_international(self) -> bool:
        """Определяет международный статус рейса по кодам аэропортов."""
        return self.origin[:2] != self.destination[:2]

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"FlightPlan({self.origin} -> {self.destination}, time={self.scheduled_time.isoformat()})"
