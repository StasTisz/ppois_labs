from __future__ import annotations

from lab3.domain.people.employee import Employee


class Dispatcher(Employee):
    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, clearance_level: int
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.clearance_level = clearance_level
        self.active_channels: int = 0

    def perform_duty(self) -> str:
        self.active_channels = 3
        return f"Диспетчер {self.full_name} ведет радиообмен на {self.active_channels} каналах."
