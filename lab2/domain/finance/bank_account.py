from __future__ import annotations

import uuid

from lab2.domain.exceptions import AccountBlockedException, InsufficientFundsException
from lab2.domain.people.person import Person


class BankAccount:
    def __init__(self, owner: Person | str, account_number: str) -> None:
        self.account_id = str(uuid.uuid4())
        self.owner = owner if isinstance(owner, Person) else None
        self.owner_id = owner.person_id if isinstance(owner, Person) else str(owner)
        self.account_number = account_number
        self.balance = 0.0
        self.is_blocked = False
        if isinstance(owner, Person):
            owner.bank_account = self

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма пополнения должна быть больше нуля")
        self.balance += amount

    def withdraw(self, amount: float) -> None:
        if self.is_blocked:
            raise AccountBlockedException("Операция отклонена: счет заблокирован.")
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть больше нуля")
        if self.balance < amount:
            raise InsufficientFundsException(f"Недостаточно средств. Баланс: {self.balance}")
        self.balance -= amount

    def block_account(self) -> None:
        self.is_blocked = True

    def transfer_to(self, target_account: BankAccount, amount: float) -> None:
        if self.account_id == target_account.account_id:
            raise ValueError("Нельзя перевести деньги самому себе.")
        self.withdraw(amount)
        target_account.deposit(amount)
