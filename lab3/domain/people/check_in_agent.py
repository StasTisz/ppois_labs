from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.passenger import Passenger


class CheckInAgent(Employee):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        assigned_counter: int | None = None,
        typing_speed: int = 150,
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.assigned_counter = assigned_counter
        self.typing_speed = typing_speed
        self._passengers_processed = 0

    @property
    def passengers_processed(self) -> int:
        return self._passengers_processed

    def perform_duty(self) -> str:
        self._passengers_processed += 1
        counter_str = (
            f"на стойке #{self.assigned_counter}"
            if self.assigned_counter
            else "в зале вылета"
        )
        return f"Агент {self.full_name} регистрирует пассажиров и багаж {counter_str} (итого: {self._passengers_processed})."

    def issue_boarding_pass(self, passenger: Passenger, flight: Flight) -> None:
        if not self.is_on_shift:
            raise ValueError(f"Агент {self.full_name} не на смене.")
        self._passengers_processed += 1

    def tag_baggage(self, baggage: Baggage) -> None:
        if not self.is_on_shift:
            raise ValueError(f"Агент {self.full_name} не на смене.")
        baggage.check_weight()
