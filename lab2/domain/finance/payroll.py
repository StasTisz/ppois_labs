from __future__ import annotations

from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.people.employee import Employee
from lab2.domain.people.student import Student


class Payroll:
    DEFAULT_SCHOLARSHIP = 120.0

    def __init__(self, month: int, year: int) -> None:
        self.month = month
        self.year = year
        self.total_fund = 0.0
        self._processed_payments: list[str] = []

    def pay_salary(self, employee: Employee, account: BankAccount, bonus: float = 0.0) -> None:
        amount = employee.salary + bonus
        account.deposit(amount)
        self.total_fund += amount
        self._processed_payments.append(f"Выплачено {amount} сотруднику {employee.full_name}")

    def pay_scholarship(
            self, student: Student, account: BankAccount, base_amount: float = DEFAULT_SCHOLARSHIP
    ) -> None:
        if not student.has_scholarship:
            raise ValueError(f"Студенту {student.full_name} не назначена стипендия")
        account.deposit(base_amount)
        self.total_fund += base_amount
        self._processed_payments.append(f"Стипендия {base_amount} студенту {student.full_name}")

    @property
    def total_payments_count(self) -> int:
        return len(self._processed_payments)

    def get_payment_history(self) -> list[str]:
        return self._processed_payments.copy()
