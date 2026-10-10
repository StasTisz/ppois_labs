from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class AcademicCertificate(Document):
    """
    Справка об обучении (например, по месту требования).
    Не требует метода execute, так как имеет исключительно информационный характер.

    Attributes:
        student (Student): Студент, на которого выдана справка.
        destination (str): Место требования.
    """

    def __init__(self, student: Student, destination: str) -> None:
        super().__init__(f"Справка об обучении: {student.full_name}")
        self.student = student
        self.destination = destination
