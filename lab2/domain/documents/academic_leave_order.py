from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class AcademicLeaveOrder(Document):
    ALLOWED_DURATIONS_MONTHS = (6, 12, 24)

    def __init__(
        self,
        student: Student,
        reason: str,
        duration_months: int,
        registration_number: str = "",
    ) -> None:
        super().__init__(
            f"Академический отпуск: {student.full_name}",
            registration_number=registration_number,
        )
        self.student = student
        self.reason = reason
        self.duration_months = duration_months

    def is_eligible(self) -> bool:
        return self.student.is_active and self.duration_months in self.ALLOWED_DURATIONS_MONTHS

    def execute(self) -> None:
        self._ensure_signed()
        if not self.student.is_active:
            raise ValueError(
                f"Студент {self.student.full_name} уже не числится активным."
            )
        self.student.grant_academic_leave(self.duration_months)
