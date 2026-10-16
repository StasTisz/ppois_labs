"""Модуль договора на платное обучение студента."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.finance.bank_account import BankAccount
    from lab2.domain.people.student import Student


class TuitionContract:
    """Договор на платное обучение студента."""

    MIN_DISCOUNT_PERCENT = 0.0
    MAX_DISCOUNT_PERCENT = 100.0
    OVERDUE_RATIO = 0.5

    def __init__(
        self,
        number: str,
        student: Student,
        total_amount: float,
        bank_account: BankAccount | None = None,
    ) -> None:
        """Инициализирует экземпляр класса TuitionContract."""
        self.number = number
        self.student = student
        self.bank_account = bank_account or getattr(student, "bank_account", None)
        self._total_amount = total_amount
        self._paid_amount = 0.0
        self._is_signed = False
        self.creation_date = datetime.now(UTC)

    @property
    def total_amount(self) -> float:
        """Возвращает значение атрибута total_amount."""
        return self._total_amount

    @property
    def paid_amount(self) -> float:
        """Возвращает значение атрибута paid_amount."""
        return self._paid_amount

    @property
    def is_signed(self) -> bool:
        """Возвращает признак signed."""
        return self._is_signed

    def _sync_student_debt(self) -> None:
        """Внутренний помощник: синхронизирует задолженность с профилем студента."""
        self.student.apply_financial_debt(self.debt)

    def attach_bank_account(self, account: BankAccount) -> None:
        """Привязывает расчетный банковский счет к договору на обучение."""
        self.bank_account = account

    def sign_contract(self) -> None:
        """Утверждает договор и фиксирует финансовую задолженность за студентом."""
        self._is_signed = True
        self._sync_student_debt()

    @property
    def debt(self) -> float:
        """Агрегация: вычисляет текущий остаток неоплаченного долга."""
        return max(0.0, round(self._total_amount - self._paid_amount, 2))

    @property
    def is_fully_paid(self) -> bool:
        """Бизнес-правило: проверяет, погашена ли задолженность полностью."""
        return self.debt <= 0.0

    def pay_tuition(self, amount: float, account: BankAccount | None = None) -> None:
        """Оплачивает обучение путем безналичного списания со счета."""
        if not self._is_signed:
            raise ValueError("Нельзя оплатить неподписанный договор")
        target_account = account or self.bank_account
        if target_account is None:
            raise ValueError("Не указан банковский счет для списания средств.")
        target_account.withdraw(amount)
        self._paid_amount = round(self._paid_amount + amount, 2)
        self._sync_student_debt()

    def apply_discount(self, percent: float) -> None:
        """Применяет скидку на общую стоимость обучения."""
        if not (self.MIN_DISCOUNT_PERCENT < percent <= self.MAX_DISCOUNT_PERCENT):
            raise ValueError(
                f"Процент скидки должен быть от {self.MIN_DISCOUNT_PERCENT} до {self.MAX_DISCOUNT_PERCENT}."
            )
        discount_amount = self._total_amount * (percent / 100.0)
        self._total_amount = round(self._total_amount - discount_amount, 2)
        self._sync_student_debt()

    @property
    def is_overdue(self) -> bool:
        """Бизнес-правило: проверяет, является ли платеж просроченным.
        Просрочка фиксируется, если внесено менее установленного порога (50% по умолчанию)."""
        min_required_payment = self._total_amount * self.OVERDUE_RATIO
        return self._paid_amount < min_required_payment

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"TuitionContract(num={self.number!r}, student={self.student.full_name!r}, total={self._total_amount}, paid={self._paid_amount})"
