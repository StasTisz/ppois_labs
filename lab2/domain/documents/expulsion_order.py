from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.exceptions import ExpulsionDeniedException
from lab2.domain.people.student import Student


class ExpulsionOrder(Document):
    """
    Приказ об отчислении студента.

    Attributes:
        student (Student): Отчисляемый студент.
        reason (str): Основание для отчисления.
    """

    def __init__(self, student: Student, reason: str) -> None:
        super().__init__(f"Приказ об отчислении: {student.full_name}")
        self.student = student
        self.reason = reason

    def execute(self) -> None:
        """
        Применяет приказ: проверяет законность оснований и меняет статус студента.

        Raises:
            ExpulsionDeniedException: Если нет веских причин для отчисления.
        """
        self._ensure_signed()

        reason_lower = self.reason.lower()
        has_academic_ground = "академическ" in reason_lower or "неуспеваемост" in reason_lower
        is_voluntary = "по собственному" in reason_lower

        if self.student.financial_debt == 0.0 and not has_academic_ground and not is_voluntary:
            raise ExpulsionDeniedException(f"Нет оснований для отчисления студента {self.student.full_name}")

        self.student.expel()
