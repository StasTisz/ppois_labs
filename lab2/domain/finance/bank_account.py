from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.exceptions import AccountBlockedException, InsufficientFundsException

if TYPE_CHECKING:
    from lab2.domain.people.person import Person


class BankAccount:
    def __init__(self, owner: Person, account_number: str) -> None:
        self.owner = owner
        self.account_number = account_number
        self._balance = 0.0
        self._is_blocked = False
        if hasattr(owner, "bank_account"):
            owner.bank_account = self

    @property
    def owner_id(self) -> str:
        if hasattr(self.owner, "passport_number"):
            return self.owner.passport_number
        if hasattr(self.owner, "person_id"):
            return self.owner.person_id
        return str(self.owner)

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def is_blocked(self) -> bool:
        return self._is_blocked

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self._balance = round(self._balance + amount, 2)

    def withdraw(self, amount: float) -> None:
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
        self._is_blocked = True

    def unblock_account(self) -> None:
        self._is_blocked = False

    def transfer_to(self, target_account: BankAccount, amount: float) -> None:
        if self.account_number == target_account.account_number:
            raise ValueError("Нельзя перевести деньги самому себе.")
        self.withdraw(amount)
        target_account.deposit(amount)

    def __str__(self) -> str:
        return (
            f"Счет #{self.account_number} ({self.owner.full_name}): {self._balance} BYN"
        )

    def __repr__(self) -> str:
        return f"BankAccount(number={self.account_number!r}, owner={self.owner.full_name!r}, balance={self._balance})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.account_number == other.account_number

    def __hash__(self) -> int:
        return hash(self.account_number)
