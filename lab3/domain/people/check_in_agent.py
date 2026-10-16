"""Модуль агента по регистрации пассажиров и багажа."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.passenger import Passenger


class CheckInAgent(Employee):
    """Агент службы организации перевозок (работает за стойкой)."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        assigned_counter: int | None = None,
        typing_speed: int = 150,
    ) -> None:
        """Инициализирует экземпляр класса CheckInAgent."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.assigned_counter = assigned_counter
        self.typing_speed = typing_speed
        self._passengers_processed = 0

    @property
    def passengers_processed(self) -> int:
        """Количество зарегистрированных агентом пассажиров за смену."""
        return self._passengers_processed

    def perform_duty(self) -> str:
        """Оформляет пассажира на рейс."""
        self._passengers_processed += 1
        counter_str = (
            f"на стойке #{self.assigned_counter}"
            if self.assigned_counter
            else "в зале вылета"
        )
        return f"Агент {self.full_name} регистрирует пассажиров и багаж {counter_str} (итого: {self._passengers_processed})."

    def issue_boarding_pass(self, passenger: Passenger, flight: Flight) -> None:
        """Оформляет и выдает посадочный талон пассажиру на стойке регистрации."""
        if not self.is_on_shift:
            raise ValueError(f"Агент {self.full_name} не на смене.")
        self._passengers_processed += 1

    def tag_baggage(self, baggage: Baggage) -> None:
        """Маркирует сдаваемый багаж пассажира багажной биркой."""
        if not self.is_on_shift:
            raise ValueError(f"Агент {self.full_name} не на смене.")
        baggage.check_weight()
