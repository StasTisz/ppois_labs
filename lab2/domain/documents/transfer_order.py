from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup


class TransferOrder(Document):
    def __init__(self, student: Student, from_group: AcademicGroup, to_group: AcademicGroup) -> None:
        super().__init__(f"Приказ о переводе: {student.full_name}")
        self.student = student
        self.from_group = from_group
        self.to_group = to_group

    def execute(self) -> None:
        self._ensure_signed()
        self.from_group.expel_student(self.student)
        self.to_group.enroll_student(self.student)
