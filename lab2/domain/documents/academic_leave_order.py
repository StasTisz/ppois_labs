from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class AcademicLeaveOrder(Document):
    def __init__(self, student: Student, reason: str, duration_months: int) -> None:
        super().__init__(f"Академический отпуск: {student.full_name}")
        self.student = student
        self.reason = reason
        self.duration_months = duration_months

    def execute(self) -> None:
        self._ensure_signed()
        self.student.is_active = False
        self.student.has_scholarship = False
