from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ScholarshipOrder(Document):
    def __init__(self, students: list[Student], registration_number: str = "") -> None:
        super().__init__(
            f"Приказ о стипендии ({len(students)} чел.)",
            registration_number=registration_number,
        )
        self._students = list(students)

    @property
    def students(self) -> list[Student]:
        return list(self._students)

    def add_student(self, student: Student) -> None:
        if not student.is_active:
            raise ValueError(
                f"Нельзя назначить стипендию неактивному студенту {student.full_name}"
            )
        if student not in self._students:
            self._students.append(student)

    def remove_student(self, student: Student) -> None:
        if student in self._students:
            self._students.remove(student)

    def execute(self) -> None:
        self._ensure_signed()
        for student in self._students:
            student.grant_scholarship()
