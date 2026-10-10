from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ReprimandOrder(Document):
    """
    Приказ о выговоре за нарушение устава вуза или правил общежития.

    Attributes:
        student (Student): Студент, получающий выговор.
        reason (str): Причина наказания.
        is_strict (bool): Является ли выговор строгим (с лишением стипендии).
    """

    def __init__(self, student: Student, reason: str, is_strict: bool = False) -> None:
        super().__init__(f"Приказ о выговоре: {student.full_name}")
        self.student = student
        self.reason = reason
        self.is_strict = is_strict

    def execute(self) -> None:
        """Применяет санкции к студенту (лишение стипендии при строгом выговоре)."""
        self._ensure_signed()

        if self.is_strict and self.student.has_scholarship:
            self.student.has_scholarship = False
