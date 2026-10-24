"""Модуль архивной академической справки."""

from __future__ import annotations

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class AcademicCertificate(Document):
    """Справка об обучении (например, по месту требования).
    Не требует метода execute, так как имеет исключительно информационный характер."""

    def __init__(
        self,
        student: Student,
        destination: str,
        purpose: str = "По месту требования",
        registration_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса AcademicCertificate."""
        super().__init__(
            f"Справка об обучении: {student.full_name}",
            registration_number=registration_number,
        )
        self.student = student
        self.destination = destination
        self.purpose = purpose

    def verify_student_status(self) -> bool:
        """Проверяет актуальность статуса студента перед формированием справки."""
        return self.student.is_active

    def generate_text(self) -> str:
        """Генерирует официальный текст академической архивной справки."""
        status = (
            "действительно является студентом" if self.student.is_active else "отчислен"
        )
        group_num = self.student.group.number if self.student.group else "без группы"
        return (
            f"СПРАВКА #{self.registration_number}\n"
            f"Дана студенту {self.student.full_name} (зачетка {self.student.record_book_number})\n"
            f"в том, что он {status} группы {group_num}.\n"
            f"Выдана для предоставления: {self.destination} ({self.purpose})."
        )

    def issue(self) -> str:
        """Выдает академическую справку студенту с фиксацией в реестре."""
        self._ensure_signed()
        if not self.verify_student_status():
            raise ValueError(
                f"Нельзя выдать справку об обучении отчисленному студенту {self.student.full_name}."
            )
        return self.generate_text()
