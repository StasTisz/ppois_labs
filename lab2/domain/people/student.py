from __future__ import annotations

from typing import Any

from lab2.domain.people.person import Person


class Student(Person):
    """
    Студент университета.

    Attributes:
        record_book_number (str): Номер зачетной книжки.
        record_book (Any): Зачетная книжка студента (объект RecordBook).
        group (Any): Учебная группа студента (объект AcademicGroup).
        room (Any): Комната в общежитии (объект Room).
        library_card (Any): Читательский билет студента (объект LibraryCard).
        is_active (bool): Статус обучения (False, если отчислен или в академе).
        has_scholarship (bool): Наличие академической стипендии.
        financial_debt (float): Текущий долг за платное обучение или общежитие.
    """

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
        """Отчисляет студента, деактивируя его статус и лишая стипендии."""
        self.is_active = False
        self.has_scholarship = False

    def grant_scholarship(self) -> None:
        """
        Назначает академическую стипендию.

        Raises:
            ValueError: Если попытка назначить стипендию неактивному (отчисленному) студенту.
        """
        if not self.is_active:
            raise ValueError(f"Нельзя назначить стипендию отчисленному студенту {self.full_name}")
        self.has_scholarship = True

    @property
    def is_debtor(self) -> bool:
        """Проверяет, имеет ли студент непогашенную финансовую задолженность."""
        return self.financial_debt > 0.0

    def pay_debt(self, amount: float) -> None:
        """
        Частично или полностью погашает финансовую задолженность студента.

        Args:
            amount (float): Сумма внесенного платежа.

        Raises:
            ValueError: Если сумма платежа отрицательная или равна нулю.
        """
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной.")
        if amount > self.financial_debt:
            self.financial_debt = 0.0
        else:
            self.financial_debt -= amount
