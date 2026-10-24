"""Модуль инспектора службы авиационной безопасности."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class SecurityOfficer(Employee):
    """Офицер службы авиационной безопасности (САБ)."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        badge_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса SecurityOfficer."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.badge_number = badge_number or f"SEC-{passport_number[-4:]}"
        self._detained_passengers: list[Passenger] = []

    @property
    def detained_passengers(self) -> list[Passenger]:
        """Возвращает значение атрибута detained_passengers."""
        return list(self._detained_passengers)

    def perform_duty(self) -> str:
        """Осуществляет досмотр пассажиров и багажа."""
        return f"Офицер СБ {self.full_name} [Жетон: {self.badge_number}] осуществляет досмотр в зоне контроля."

    def detain_passenger(self, passenger: Passenger, reason: str) -> None:
        """Задерживает нарушителя на пункте досмотра для разбирательства."""
        if not reason.strip():
            raise ValueError("Причина задержания не указана.")
        if passenger not in self._detained_passengers:
            self._detained_passengers.append(passenger)

    def release_passenger(self, passenger: Passenger) -> None:
        """Освобождает задержанного пассажира после проверки документов."""
        if passenger in self._detained_passengers:
            self._detained_passengers.remove(passenger)
