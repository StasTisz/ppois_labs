from __future__ import annotations

from lab2.domain.people.person import Person


class Employee(Person):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        position: str = "",
        passport_number: str = "",
    ) -> None:
        super().__init__(first_name, last_name, middle_name, passport_number)
        self.position = position
        self._salary = 0.0
        self._is_on_leave = False

    @property
    def salary(self) -> float:
        return self._salary

    @salary.setter
    def salary(self, value: float) -> None:
        self.change_salary(value)

    @property
    def is_on_leave(self) -> bool:
        return self._is_on_leave

    def promote(self, new_position: str, salary_increase: float = 0.0) -> None:
        if not new_position.strip():
            raise ValueError("Название должности не может быть пустым.")
        self.position = new_position
        if salary_increase > 0:
            self._salary += salary_increase

    def change_salary(self, new_salary: float) -> None:
        if new_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")
        self._salary = new_salary

    def grant_leave(self) -> None:
        self._is_on_leave = True

    def return_from_leave(self) -> None:
        self._is_on_leave = False
