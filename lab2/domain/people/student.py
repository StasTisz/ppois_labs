from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.people.person import Person

if TYPE_CHECKING:
    from lab2.domain.grading.record_book import RecordBook
    from lab2.domain.infrastructure.room import Room
    from lab2.domain.library.library_card import LibraryCard
    from lab2.domain.structure.academic_group import AcademicGroup


class Student(Person):
    def __init__(self, first_name: str, last_name: str, middle_name: str = "", record_book_number: str = "") -> None:
        super().__init__(first_name, last_name, middle_name)
        self.record_book_number = record_book_number
        self.record_book: RecordBook | None = None
        self.group: AcademicGroup | None = None
        self.room: Room | None = None
        self.library_card: LibraryCard | None = None
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
