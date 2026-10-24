"""Модуль лицевого банковского счета."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import AccountBlockedException, InsufficientFundsException

if TYPE_CHECKING:
    from lab2.domain.people.person import Person


class BankAccount:
    """Счет студента или сотрудника для начислений и оплат."""

    def __init__(self, owner: Person, account_number: str) -> None:
        """Инициализирует экземпляр класса BankAccount."""
        self.owner = owner
        self.account_number = account_number
        self._balance = 0.0
        self._is_blocked = False
        if hasattr(owner, "bank_account"):
            owner.bank_account = self

    @property
    def balance(self) -> float:
        """Возвращает значение атрибута balance."""
        return self._balance

    @property
    def is_blocked(self) -> bool:
        """Возвращает признак blocked."""
        return self._is_blocked

    def deposit(self, amount: float) -> None:
        """Пополняет счет на указанную сумму."""
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self._balance = round(self._balance + amount, 2)

    def withdraw(self, amount: float) -> None:
        """Списывает средства со счета с проверкой блокировки и баланса."""
        if self._is_blocked:
            raise AccountBlockedException("Операция отклонена: счет заблокирован.")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if self._balance < amount:
            raise InsufficientFundsException(
                f"Недостаточно средств. Баланс: {self._balance}"
            )
        self._balance = round(self._balance - amount, 2)

    def block_account(self) -> None:
        """Блокирует счет от любых расходных операций."""
        self._is_blocked = True

    def unblock_account(self) -> None:
        """Снимает блокировку с банковского счета."""
        self._is_blocked = False

    def transfer_to(self, target_account: BankAccount, amount: float) -> None:
        """Выполняет перевод средств на другой счет (транзакция)."""
        if self.account_number == target_account.account_number:
            raise ValueError("Нельзя перевести деньги самому себе.")
        self.withdraw(amount)
        target_account.deposit(amount)

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (
            f"Счет #{self.account_number} ({self.owner.full_name}): {self._balance} BYN"
        )

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"BankAccount(number={self.account_number!r}, owner={self.owner.full_name!r}, balance={self._balance})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.account_number == other.account_number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.account_number)
