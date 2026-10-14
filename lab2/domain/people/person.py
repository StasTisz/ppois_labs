from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.finance.bank_account import BankAccount


class Person:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        passport_number: str = "",
    ) -> None:
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.passport_number = (
            passport_number or f"MP{abs(hash((first_name, last_name))) % 10000000:07d}"
        )
        self._bank_account: BankAccount | None = None

    @property
    def person_id(self) -> str:
        return self.passport_number

    @property
    def full_name(self) -> str:
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    @property
    def bank_account(self) -> BankAccount | None:
        return self._bank_account

    @bank_account.setter
    def bank_account(self, account: BankAccount | None) -> None:
        self._bank_account = account

    def attach_bank_account(self, account: BankAccount) -> None:
        self._bank_account = account

    def detach_bank_account(self) -> None:
        self._bank_account = None

    def change_last_name(self, new_last_name: str) -> None:
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name

    def __str__(self) -> str:
        return self.full_name

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.full_name!r}, passport={self.passport_number!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Person):
            return NotImplemented
        return self.passport_number == other.passport_number

    def __hash__(self) -> int:
        return hash(self.passport_number)
