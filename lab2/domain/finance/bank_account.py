from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.people.person import Person


class BankAccount:
    """
    Счет студента или сотрудника для начислений и оплат.

    Attributes:
        account_id (str): Уникальный внутренний идентификатор (UUID).
        owner (Person | None): Объект владельца счета (Student или Employee).
        owner_id (str): Идентификатор владельца (Student.person_id или Employee.person_id).
        account_number (str): Уникальный банковский номер счета.
        balance (float): Текущий баланс.
        is_blocked (bool): Статус блокировки счета.
    """

    def __init__(self, owner: Person | str, account_number: str) -> None:
        self.account_id = str(uuid.uuid4())
        self.owner = owner if not isinstance(owner, str) else None
        self.owner_id = getattr(owner, "person_id", str(owner))
        self.account_number = account_number
        self.balance = 0.0
        self.is_blocked = False
        if hasattr(owner, "bank_account"):
            owner.bank_account = self

    def deposit(self, amount: float) -> None:
        """
        Пополняет счет на указанную сумму.

        Args:
            amount (float): Сумма пополнения.

        Raises:
            ValueError: Если сумма нулевая или отрицательная.
        """
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        """
        Списывает средства со счета с проверкой блокировки и баланса.

        Args:
            amount (float): Сумма списания.

        Raises:
            ValueError: Если счет заблокирован, сумма <= 0 или недостаточно средств.
        """
        if self.is_blocked:
            raise ValueError("Операция отклонена: счет заблокирован")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if self.balance < amount:
            raise ValueError(f"Недостаточно средств. Баланс: {self.balance}")
        self.balance -= amount

    def block_account(self) -> None:
        """Блокирует счет от любых расходных операций."""
        self.is_blocked = True

    def transfer_to(self, target_account: BankAccount, amount: float) -> None:
        """
        Выполняет перевод средств на другой счет (транзакция).

        Args:
            target_account (BankAccount): Счет получателя.
            amount (float): Сумма перевода.

        Raises:
            ValueError: При попытке перевести деньги самому себе.
        """
        if self.account_id == target_account.account_id:
            raise ValueError("Нельзя перевести деньги самому себе.")

        self.withdraw(amount)
        target_account.deposit(amount)
