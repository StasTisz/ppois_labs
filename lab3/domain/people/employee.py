from __future__ import annotations

from abc import ABC, abstractmethod

from lab3.domain.people.person import Person


class Employee(Person, ABC):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
    ) -> None:
        super().__init__(first_name, last_name, passport_number)
        self.employee_id = f"EMP-{passport_number}"
        self.salary = salary
        self.is_on_shift = False

    def clock_in(self) -> None:
        self.is_on_shift = True

    def clock_out(self) -> None:
        self.is_on_shift = False

    def adjust_salary(self, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")
        self.salary = new_salary

    @abstractmethod
    def perform_duty(self) -> str:
        """Полиморфный метод выполнения профессиональных обязанностей."""
