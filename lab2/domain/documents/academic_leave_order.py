"""Модуль приказа о предоставлении академического отпуска."""

from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class AcademicLeaveOrder(Document):
    """Приказ о предоставлении академического отпуска."""

    ALLOWED_DURATIONS_MONTHS = (6, 12, 24)

    def __init__(
        self,
        student: Student,
        reason: str,
        duration_months: int,
        registration_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса AcademicLeaveOrder."""
        super().__init__(
            f"Академический отпуск: {student.full_name}",
            registration_number=registration_number,
        )
        self.student = student
        self.reason = reason
        self.duration_months = duration_months

    def is_eligible(self) -> bool:
        """Проверяет соответствие студента критериям предоставления академического отпуска."""
        return (
            self.student.is_active
            and self.duration_months in self.ALLOWED_DURATIONS_MONTHS
        )

    def execute(self) -> None:
        """Замораживает статус студента (отключает стипендию и переводит в неактивный статус)."""
        self._ensure_signed()
        if not self.student.is_active:
            raise ValueError(
                f"Студент {self.student.full_name} уже не числится активным."
            )
        self.student.grant_academic_leave(self.duration_months)
