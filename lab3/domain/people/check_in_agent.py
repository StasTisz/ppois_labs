from __future__ import annotations

from lab3.domain.people.employee import Employee


class CheckInAgent(Employee):
    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, typing_speed: int
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.typing_speed = typing_speed
        self._passengers_processed = 0

    @property
    def passengers_processed(self) -> int:
        return self._passengers_processed

    def perform_duty(self) -> str:
        self._passengers_processed += 1
        return f"Агент {self.full_name} зарегистрировал пассажира (итого: {self._passengers_processed})."
