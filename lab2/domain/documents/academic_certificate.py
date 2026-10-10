from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class AcademicCertificate(Document):
    def __init__(self, student: Student, destination: str) -> None:
        super().__init__(f"Справка об обучении: {student.full_name}")
        self.student = student
        self.destination = destination
