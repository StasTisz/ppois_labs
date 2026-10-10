from __future__ import annotations

import uuid
from datetime import datetime, timezone

from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.people.student import Student


class TuitionContract:
    """
    Договор на платное обучение студента.

    Attributes:
        contract_id (str): Внутренний идентификатор договора (UUID).
        number (str): Регистрационный номер договора.
        student (Student): Студент-заказчик.
        total_amount (float): Полная стоимость обучения.
        paid_amount (float): Внесенная сумма.
        is_signed (bool): Статус подписания договора.
        creation_date (datetime): Точная дата и время создания (в UTC).
    """
    MIN_DISCOUNT_PERCENT = 0.0
    MAX_DISCOUNT_PERCENT = 100.0
    OVERDUE_RATIO = 0.5

    def __init__(self, number: str, student: Student, total_amount: float) -> None:
        self.contract_id = str(uuid.uuid4())
        self.number = number
        self.student = student
        self.total_amount = total_amount
        self.paid_amount = 0.0
        self.is_signed = False
        self.creation_date = datetime.now(timezone.utc)

    def _sync_student_debt(self) -> None:
        """Внутренний помощник: синхронизирует задолженность с профилем студента."""
        self.student.financial_debt = self.debt

    def sign_contract(self) -> None:
        """Утверждает договор и фиксирует финансовую задолженность за студентом."""
        self.is_signed = True
        self._sync_student_debt()

    @property
    def debt(self) -> float:
        """Агрегация: вычисляет текущий остаток неоплаченного долга."""
        return self.total_amount - self.paid_amount

    @property
    def is_fully_paid(self) -> bool:
        """Бизнес-правило: проверяет, погашена ли задолженность полностью."""
        return self.debt <= 0

    def pay_tuition(self, amount: float, account: BankAccount) -> None:
        """
        Оплачивает обучение путем безналичного списания со счета.

        Args:
            amount (float): Сумма платежа.
            account (BankAccount): Банковский счет, с которого списываются средства.

        Raises:
            ValueError: Если договор еще не подписан.
        """
        if not self.is_signed:
            raise ValueError("Нельзя оплатить неподписанный договор")

        account.withdraw(amount)
        self.paid_amount += amount
        self._sync_student_debt()

    def apply_discount(self, percent: float) -> None:
        """
        Применяет скидку на общую стоимость обучения.

        Args:
            percent (float): Размер скидки в процентах (от 0 до 100).

        Raises:
            ValueError: Если процент выходит за допустимые границы.
        """
        if not (self.MIN_DISCOUNT_PERCENT < percent <= self.MAX_DISCOUNT_PERCENT):
            raise ValueError(
                f"Процент скидки должен быть от {self.MIN_DISCOUNT_PERCENT} до {self.MAX_DISCOUNT_PERCENT}."
            )
        discount_amount = self.total_amount * (percent / 100)
        self.total_amount -= discount_amount
        self._sync_student_debt()

    @property
    def is_overdue(self) -> bool:
        """
        Бизнес-правило: проверяет, является ли платеж просроченным.
        Просрочка фиксируется, если внесено менее установленного порога (50% по умолчанию).
        """
        min_required_payment = self.total_amount * self.OVERDUE_RATIO
        return self.paid_amount < min_required_payment
