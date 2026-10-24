"""Модуль студента университета."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.people.person import Person

if TYPE_CHECKING:
    from lab2.domain.grading.record_book import RecordBook
    from lab2.domain.infrastructure.room import Room
    from lab2.domain.library.library_card import LibraryCard
    from lab2.domain.structure.academic_group import AcademicGroup


class Student(Person):
    """Студент университета."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        record_book_number: str = "",
        passport_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса Student."""
        super().__init__(first_name, last_name, middle_name, passport_number)
        self.record_book_number = (
            record_book_number
            or f"RB-{abs(hash((first_name, last_name, self.passport_number))) % 1000000:06d}"
        )
        self._record_book: RecordBook | None = None
        self._group: AcademicGroup | None = None
        self._room: Room | None = None
        self._library_card: LibraryCard | None = None
        self._is_active = True
        self._has_scholarship = False
        self._financial_debt = 0.0

    @property
    def is_active(self) -> bool:
        """Возвращает признак active."""
        return self._is_active

    @is_active.setter
    def is_active(self, value: bool) -> None:
        """Устанавливает значение атрибута is_active."""
        if value:
            self.reinstate()
        else:
            self.expel()

    @property
    def has_scholarship(self) -> bool:
        """Возвращает признак наличия scholarship."""
        return self._has_scholarship

    @has_scholarship.setter
    def has_scholarship(self, value: bool) -> None:
        """Устанавливает значение атрибута has_scholarship."""
        if value:
            self.grant_scholarship()
        else:
            self.revoke_scholarship()

    @property
    def financial_debt(self) -> float:
        """Возвращает значение атрибута financial_debt."""
        return self._financial_debt

    @financial_debt.setter
    def financial_debt(self, value: float) -> None:
        """Устанавливает значение атрибута financial_debt."""
        if value > self._financial_debt:
            self.apply_financial_debt(value - self._financial_debt)
        elif value < self._financial_debt:
            self.pay_debt(self._financial_debt - value)

    @property
    def is_debtor(self) -> bool:
        """Проверяет, имеет ли студент непогашенную финансовую задолженность."""
        return self._financial_debt > 0.0

    @property
    def record_book(self) -> RecordBook | None:
        """Возвращает значение атрибута record_book."""
        return self._record_book

    @record_book.setter
    def record_book(self, rb: RecordBook | None) -> None:
        """Устанавливает значение атрибута record_book."""
        self._record_book = rb

    @property
    def group(self) -> AcademicGroup | None:
        """Возвращает значение атрибута group."""
        return self._group

    @group.setter
    def group(self, target_group: AcademicGroup | None) -> None:
        """Устанавливает значение атрибута group."""
        self._group = target_group

    @property
    def room(self) -> Room | None:
        """Возвращает значение атрибута room."""
        return self._room

    @room.setter
    def room(self, target_room: Room | None) -> None:
        """Устанавливает значение атрибута room."""
        self._room = target_room

    @property
    def library_card(self) -> LibraryCard | None:
        """Возвращает значение атрибута library_card."""
        return self._library_card

    @library_card.setter
    def library_card(self, card: LibraryCard | None) -> None:
        """Устанавливает значение атрибута library_card."""
        self._library_card = card

    def expel(self) -> None:
        """Отчисляет студента, деактивируя его статус и лишая стипендии."""
        self._is_active = False
        self._has_scholarship = False

    def reinstate(self) -> None:
        """Восстанавливает отчисленного студента в ряды обучающихся."""
        self._is_active = True

    def grant_academic_leave(self, duration_months: int) -> None:
        """Предоставляет студенту академический отпуск по уважительной причине."""
        if duration_months <= 0:
            raise ValueError(
                "Длительность академического отпуска должна быть положительной."
            )
        self._is_active = False
        self._has_scholarship = False

    def grant_scholarship(self) -> None:
        """Назначает академическую стипендию."""
        if not self._is_active:
            raise ValueError(
                f"Нельзя назначить стипендию отчисленному студенту {self.full_name}"
            )
        self._has_scholarship = True

    def revoke_scholarship(self) -> None:
        """Прекращает начисление академической стипендии студенту."""
        self._has_scholarship = False

    def apply_financial_debt(self, amount: float) -> None:
        """Начисляет финансовую задолженность за обучение по контракту."""
        if amount < 0:
            raise ValueError("Сумма задолженности не может быть отрицательной.")
        self._financial_debt = round(amount, 2)

    def pay_debt(self, amount: float) -> None:
        """Частично или полностью погашает финансовую задолженность студента."""
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной.")
        if amount >= self._financial_debt:
            self._financial_debt = 0.0
        else:
            self._financial_debt = round(self._financial_debt - amount, 2)

    def assign_to_group(self, group: AcademicGroup | None) -> None:
        """Зачисляет студента в состав академической группы."""
        self._group = group

    def assign_room(self, room: Room | None) -> None:
        """Заселяет студента в указанную комнату общежития."""
        self._room = room

    def attach_library_card(self, card: LibraryCard | None) -> None:
        """Привязывает читательский билет к профилю студента."""
        self._library_card = card

    def __eq__(self, other: object) -> bool:
        """Проверяет равенство объектов по ключевым атрибутам."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.record_book_number == other.record_book_number

    def __hash__(self) -> int:
        """Вычисляет хеш-код объекта."""
        return hash(self.record_book_number)
