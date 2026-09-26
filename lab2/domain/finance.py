import uuid
from datetime import datetime

from lab2.domain.people import Employee, Student


class BankAccount:
    """Счет студента или сотрудника для начислений и оплат."""

    def __init__(self, owner_id: str, account_number: str):
        self.account_id = str(uuid.uuid4())
        self.owner_id = owner_id
        self.account_number = account_number
        self.balance = 0.0
        self.is_blocked = False

    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount: float):
        if self.is_blocked:
            raise ValueError("Операция отклонена: счет заблокирован")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if self.balance < amount:
            raise ValueError(f"Недостаточно средств. Баланс: {self.balance}")
        self.balance -= amount

    def block_account(self):
        self.is_blocked = True

    def transfer_to(self, target_account: 'BankAccount', amount: float):
        """Поведение: перевод средств между счетами (транзакция)."""
        if self.account_id == target_account.account_id:
            raise ValueError("Нельзя перевести деньги самому себе.")
        # withdraw уже содержит проверки на блокировку и минус
        self.withdraw(amount)
        target_account.deposit(amount)


class TuitionContract:
    """Договор на платное обучение."""

    def __init__(self, number: str, student: Student, total_amount: float):
        self.contract_id = str(uuid.uuid4())
        self.number = number
        self.student = student  # Ассоциация со студентом
        self.total_amount = total_amount
        self.paid_amount = 0.0
        self.is_signed = False
        self.creation_date = datetime.now()

    def sign_contract(self):
        self.is_signed = True
        self.student.financial_debt = self.debt  # Синхронизируем долг со студентом

    @property
    def debt(self) -> float:
        return self.total_amount - self.paid_amount

    @property
    def is_fully_paid(self) -> bool:
        return self.debt <= 0

    def pay_tuition(self, amount: float, account: BankAccount):
        """Оплата обучения путем списания со счета."""
        if not self.is_signed:
            raise ValueError("Нельзя оплатить неподписанный договор")

        account.withdraw(amount)
        self.paid_amount += amount
        self.student.financial_debt = self.debt

    def apply_discount(self, percent: float):
        """Применение скидки на обучение (например, за отличную учебу)."""
        if not (0 < percent <= 100):
            raise ValueError("Процент скидки должен быть от 1 до 100.")
        discount_amount = self.total_amount * (percent / 100)
        self.total_amount -= discount_amount
        self.student.financial_debt = self.debt  # Обновляем долг

    @property
    def is_overdue(self) -> bool:
        """Бизнес-правило: просрочен ли платеж (если оплачено менее 50%)."""
        return self.paid_amount < (self.total_amount / 2)


class Payroll:
    """Зарплатная ведомость / стипендиальный фонд."""

    def __init__(self, month: int, year: int):
        self.month = month
        self.year = year
        self.total_fund = 0.0
        self._processed_payments: list[str] = []

    def pay_salary(self, employee: Employee, account: BankAccount, bonus: float = 0.0):
        """Выплата зарплаты сотруднику (декану или преподавателю)."""
        amount = employee.salary + bonus
        account.deposit(amount)
        self.total_fund += amount
        self._processed_payments.append(f"Выплачено {amount} сотруднику {employee.full_name}")

    def pay_scholarship(self, student: Student, account: BankAccount, base_amount: float = 120.0):
        """Выплата стипендии активному студенту без долгов."""
        if not student.has_scholarship:
            raise ValueError(f"Студенту {student.full_name} не назначена стипендия")

        account.deposit(base_amount)
        self.total_fund += base_amount
        self._processed_payments.append(f"Стипендия {base_amount} студенту {student.full_name}")

    @property
    def total_payments_count(self) -> int:
        """Агрегация: общее количество проведенных транзакций фонда."""
        return len(self._processed_payments)

    def get_payment_history(self) -> list[str]:
        """Поведение: получение копии выписки из зарплатной ведомости."""
        return self._processed_payments.copy()