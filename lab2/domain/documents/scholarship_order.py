from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ScholarshipOrder(Document):
    """
    Массовый приказ о назначении академической стипендии.

    Attributes:
        students (list[Student]): Список студентов-стипендиатов.
    """

    def __init__(self, students: list[Student]) -> None:
        super().__init__(f"Приказ о стипендии ({len(students)} чел.)")
        self.students = students

    def execute(self) -> None:
        """Выполняет массовое начисление стипендии указанным студентам."""
        self._ensure_signed()
        for student in self.students:
            student.grant_scholarship()
