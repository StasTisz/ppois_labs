"""Модуль авиадиспетчера службы управления воздушным движением."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class Dispatcher(Employee):
    """Авиадиспетчер вышки управления движением."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        rating: str = "Approach/Tower",
        clearance_level: int = 1,
    ) -> None:
        """Инициализирует экземпляр класса Dispatcher."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.rating = rating
        self.clearance_level = clearance_level
        self.active_channels = clearance_level

    def perform_duty(self) -> str:
        """Мониторит частоты и координирует взлеты/посадки."""
        self.active_channels = self.clearance_level
        return f"Диспетчер {self.full_name} ({self.rating}) координирует движение ВС на {self.active_channels} каналах."

    def coordinate_slot(self, flight: Flight) -> str:
        """Координирует слот взлета или посадки воздушного судна на ВПП."""
        if not self.is_on_shift:
            raise ValueError(f"Диспетчер {self.full_name} не на смене.")
        return f"Диспетчер {self.full_name} подтвердил слот для рейса {flight.flight_number}."

    def issue_weather_alert(self, warning: str) -> str:
        """Формирует оперативное штормовое предупреждение для экипажей."""
        if not warning.strip():
            raise ValueError("Текст метеопредупреждения не может быть пустым.")
        return f"ВНИМАНИЕ ЭКИПАЖАМ от диспетчера {self.full_name}: {warning}"
