"""Модуль базовой сущности физического лица."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.finance.bank_account import BankAccount


class Person:
    """Базовый класс для всех физических лиц в системе."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        passport_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса Person."""
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.passport_number = (
            passport_number or f"MP{abs(hash((first_name, last_name))) % 10000000:07d}"
        )
        self._bank_account: BankAccount | None = None

    @property
    def person_id(self) -> str:
        """Возвращает значение атрибута person_id."""
        return self.passport_number

    @property
    def full_name(self) -> str:
        """Возвращает полное имя персоны (Имя + Фамилия)."""
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    @property
    def bank_account(self) -> BankAccount | None:
        """Возвращает значение атрибута bank_account."""
        return self._bank_account

    @bank_account.setter
    def bank_account(self, account: BankAccount | None) -> None:
        """Устанавливает значение атрибута bank_account."""
        self._bank_account = account

    def attach_bank_account(self, account: BankAccount) -> None:
        """Привязывает лицевой банковский счет к физическому лицу."""
        self._bank_account = account

    def detach_bank_account(self) -> None:
        """Отвязывает лицевой банковский счет от физического лица."""
        self._bank_account = None

    def change_last_name(self, new_last_name: str) -> None:
        """Изменяет фамилию человека (например, при вступлении в брак)."""
        if not new_last_name.strip():
            raise ValueError("Фамилия не может быть пустой.")
        self.last_name = new_last_name

    def __str__(self) -> str:
        """Возвращает строковое представление объекта."""
        return self.full_name

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"{self.__class__.__name__}({self.full_name!r}, passport={self.passport_number!r})"

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Person):
            return NotImplemented
        return self.passport_number == other.passport_number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.passport_number)
