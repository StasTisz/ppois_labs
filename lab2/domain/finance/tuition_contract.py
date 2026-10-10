from __future__ import annotations

import uuid
from datetime import UTC, datetime

from lab2.domain.finance.bank_account import BankAccount
from lab2.domain.people.student import Student


class TuitionContract:
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
        self.creation_date = datetime.now(UTC)

    def _sync_student_debt(self) -> None:
        self.student.financial_debt = self.debt

    def sign_contract(self) -> None:
        self.is_signed = True
        self._sync_student_debt()

    @property
    def debt(self) -> float:
        return self.total_amount - self.paid_amount

    @property
    def is_fully_paid(self) -> bool:
        return self.debt <= 0

    def pay_tuition(self, amount: float, account: BankAccount) -> None:
        if not self.is_signed:
            raise ValueError("Нельзя оплатить неподписанный договор")
        account.withdraw(amount)
        self.paid_amount += amount
        self._sync_student_debt()

    def apply_discount(self, percent: float) -> None:
        if not (self.MIN_DISCOUNT_PERCENT < percent <= self.MAX_DISCOUNT_PERCENT):
            raise ValueError(
                f"Процент скидки должен быть от {self.MIN_DISCOUNT_PERCENT} до {self.MAX_DISCOUNT_PERCENT}."
            )
        discount_amount = self.total_amount * (percent / 100)
        self.total_amount -= discount_amount
        self._sync_student_debt()

    @property
    def is_overdue(self) -> bool:
        min_required_payment = self.total_amount * self.OVERDUE_RATIO
        return self.paid_amount < min_required_payment
