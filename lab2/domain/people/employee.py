from __future__ import annotations

from lab2.domain.people.person import Person


class Employee(Person):
    """
    Сотрудник университета.

    Attributes:
        position (str): Текущая должность.
        salary (float): Текущий оклад.
    """

    def __init__(self, first_name: str, last_name: str, middle_name: str = "", position: str = "") -> None:
        super().__init__(first_name, last_name, middle_name)
        self.position = position
        self.salary = 0.0

    def promote(self, new_position: str, salary_increase: float = 0.0) -> None:
        """
        Повышает сотрудника в должности с опциональным увеличением оклада.

        Args:
            new_position (str): Название новой должности.
            salary_increase (float): Сумма прибавки к окладу (по умолчанию 0.0).
        """
        self.position = new_position
        if salary_increase > 0:
            self.salary += salary_increase

    def change_salary(self, new_salary: float) -> None:
        """
        Устанавливает новый размер оклада.

        Args:
            new_salary (float): Новый размер оклада.

        Raises:
            ValueError: Если новый оклад отрицательный.
        """
        if new_salary < 0:
            raise ValueError("Оклад не может быть отрицательным.")
        self.salary = new_salary
