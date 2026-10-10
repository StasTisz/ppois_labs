from __future__ import annotations

from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.people.employee import Employee
from lab2.domain.people.student import Student


class Payroll:
    """
    Зарплатная ведомость и стипендиальный фонд для массовых выплат.

    Attributes:
        month (int): Месяц выплат.
        year (int): Год выплат.
        total_fund (float): Общая сумма выданных средств.
    """
    DEFAULT_SCHOLARSHIP = 120.0

    def __init__(self, month: int, year: int) -> None:
        self.month = month
        self.year = year
        self.total_fund = 0.0
        self._processed_payments: list[str] = []

    def pay_salary(self, employee: Employee, account: BankAccount, bonus: float = 0.0) -> None:
        """
        Выплачивает заработную плату сотруднику (включая премии).

        Args:
            employee (Employee): Получатель выплаты.
            account (BankAccount): Счет для зачисления.
            bonus (float): Дополнительная премия.
        """
        amount = employee.salary + bonus
        account.deposit(amount)
        self.total_fund += amount
        self._processed_payments.append(f"Выплачено {amount} сотруднику {employee.full_name}")

    def pay_scholarship(
            self, student: Student, account: BankAccount, base_amount: float = DEFAULT_SCHOLARSHIP
    ) -> None:
        """
        Выплачивает стипендию активному студенту без долгов.

        Args:
            student (Student): Получатель стипендии.
            account (BankAccount): Счет для зачисления.
            base_amount (float): Базовый размер выплаты.

        Raises:
            ValueError: Если студент лишен академической стипендии.
        """
        if not student.has_scholarship:
            raise ValueError(f"Студенту {student.full_name} не назначена стипендия")

        account.deposit(base_amount)
        self.total_fund += base_amount
        self._processed_payments.append(f"Стипендия {base_amount} студенту {student.full_name}")

    @property
    def total_payments_count(self) -> int:
        """Агрегация: вычисляет общее количество проведенных транзакций фонда."""
        return len(self._processed_payments)

    def get_payment_history(self) -> list[str]:
        """
        Возвращает защищенную копию выписки по ведомости.

        Returns:
            list[str]: Массив логов с историей транзакций.
        """
        return self._processed_payments.copy()
