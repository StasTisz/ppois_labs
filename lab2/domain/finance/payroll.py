"""Модуль ведомости расчета и выплаты заработной платы."""

from __future__ import annotations

from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.people.employee import Employee
from lab2.domain.people.student import Student


class Payroll:
    """Зарплатная ведомость и стипендиальный фонд для массовых выплат."""

    DEFAULT_SCHOLARSHIP = 120.0
    INCOME_TAX_RATE = 0.13

    def __init__(self, month: int, year: int) -> None:
        """Инициализирует экземпляр класса Payroll."""
        self.month = month
        self.year = year
        self._total_fund = 0.0
        self._processed_payments: list[str] = []

    @property
    def total_fund(self) -> float:
        """Возвращает значение атрибута total_fund."""
        return self._total_fund

    @property
    def total_payments_count(self) -> int:
        """Агрегация: вычисляет общее количество проведенных транзакций фонда."""
        return len(self._processed_payments)

    @property
    def processed_payments(self) -> list[str]:
        """Возвращает значение атрибута processed_payments."""
        return list(self._processed_payments)

    def calculate_tax(self, amount: float) -> float:
        """Рассчитывает подоходный налог с начисленной заработной платы."""
        if amount < 0:
            raise ValueError("Сумма для расчета налога не может быть отрицательной.")
        return round(amount * self.INCOME_TAX_RATE, 2)

    def pay_salary(
        self, employee: Employee, account: BankAccount, bonus: float = 0.0
    ) -> None:
        """Выплачивает заработную плату сотруднику (включая премии)."""
        if bonus < 0:
            raise ValueError("Премия не может быть отрицательной.")
        gross_amount = employee.salary + bonus
        account.deposit(gross_amount)
        self._total_fund = round(self._total_fund + gross_amount, 2)
        self._processed_payments.append(
            f"Выплачено {gross_amount} руб. сотруднику {employee.full_name} на счет {account.account_number}"
        )

    def pay_scholarship(
        self,
        student: Student,
        account: BankAccount,
        base_amount: float = DEFAULT_SCHOLARSHIP,
    ) -> None:
        """Выплачивает стипендию активному студенту без долгов."""
        if not student.has_scholarship:
            raise ValueError(f"Студенту {student.full_name} не назначена стипендия")
        if base_amount <= 0:
            raise ValueError("Размер стипендии должен быть больше нуля.")
        account.deposit(base_amount)
        self._total_fund = round(self._total_fund + base_amount, 2)
        self._processed_payments.append(
            f"Стипендия {base_amount} руб. студенту {student.full_name} на счет {account.account_number}"
        )

    def get_payment_history(self) -> list[str]:
        """Возвращает защищенную копию выписки по ведомости."""
        return list(self._processed_payments)
