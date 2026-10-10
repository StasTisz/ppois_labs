from __future__ import annotations

from typing import Any

from lab2.domain.people.person import Person


class Student(Person):
    def __init__(self, first_name: str, last_name: str, middle_name: str = "", record_book_number: str = "") -> None:
        super().__init__(first_name, last_name, middle_name)
        self.record_book_number = record_book_number
        self.record_book: Any = None
        self.group: Any = None
        self.room: Any = None
        self.library_card: Any = None
        self.is_active = True
        self.has_scholarship = False
        self.financial_debt = 0.0

    def expel(self) -> None:
        self.is_active = False
        self.has_scholarship = False

    def grant_scholarship(self) -> None:
        if not self.is_active:
            raise ValueError(f"Нельзя назначить стипендию отчисленному студенту {self.full_name}")
        self.has_scholarship = True

    @property
    def is_debtor(self) -> bool:
        return self.financial_debt > 0.0

    def pay_debt(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной.")
        if amount > self.financial_debt:
            self.financial_debt = 0.0
        else:
            self.financial_debt -= amount
