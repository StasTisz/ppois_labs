from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ReprimandOrder(Document):
    def __init__(self, student: Student, reason: str, is_strict: bool = False) -> None:
        super().__init__(f"Приказ о выговоре: {student.full_name}")
        self.student = student
        self.reason = reason
        self.is_strict = is_strict

    def execute(self) -> None:
        self._ensure_signed()
        if self.is_strict and self.student.has_scholarship:
            self.student.has_scholarship = False
