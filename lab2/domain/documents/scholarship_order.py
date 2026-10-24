"""Модуль приказа о назначении академической стипендии."""

from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ScholarshipOrder(Document):
    """Массовый приказ о назначении академической стипендии."""

    DEFAULT_MONTHLY_AMOUNT = 120.0
    DEFAULT_DURATION_MONTHS = 5

    def __init__(
        self,
        students: list[Student],
        registration_number: str = "",
        monthly_amount: float = DEFAULT_MONTHLY_AMOUNT,
        duration_months: int = DEFAULT_DURATION_MONTHS,
    ) -> None:
        """Инициализирует экземпляр класса ScholarshipOrder."""
        super().__init__(
            f"Приказ о стипендии ({len(students)} чел.)",
            registration_number=registration_number,
        )
        self.monthly_amount = monthly_amount
        self.duration_months = duration_months
        self._students = list(students)

    @property
    def students(self) -> list[Student]:
        """Возвращает значение атрибута students."""
        return list(self._students)

    def add_student(self, student: Student) -> None:
        """Включает студента в список получателей академической стипендии."""
        if not student.is_active:
            raise ValueError(
                f"Нельзя назначить стипендию неактивному студенту {student.full_name}"
            )
        if student not in self._students:
            self._students.append(student)

    def remove_student(self, student: Student) -> None:
        """Исключает студента из списка стипендиатов приказа."""
        if student in self._students:
            self._students.remove(student)

    def execute(self) -> None:
        """Выполняет массовое начисление стипендии указанным студентам."""
        self._ensure_signed()
        for student in self._students:
            student.grant_scholarship()
