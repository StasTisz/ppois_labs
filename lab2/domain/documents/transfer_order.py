"""Модуль приказа о переводе студента в другую группу."""

from datetime import UTC, datetime

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student
from lab2.domain.structure.academic_group import AcademicGroup


class TransferOrder(Document):
    """Приказ о переводе студента из одной академической группы в другую."""

    def __init__(
        self,
        student: Student,
        from_group: AcademicGroup,
        to_group: AcademicGroup,
        registration_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса TransferOrder."""
        super().__init__(
            f"Приказ о переводе: {student.full_name}",
            registration_number=registration_number,
        )
        self.student = student
        self.from_group = from_group
        self.to_group = to_group
        self.effective_date = datetime.now(UTC)

    def validate_transfer(self) -> bool:
        """Проверяет допустимость академического перевода между группами."""
        return self.to_group.has_vacancies and self.from_group.has_student(self.student)

    def execute(self) -> None:
        """Осуществляет физическое перемещение студента между группами."""
        self._ensure_signed()
        if not self.validate_transfer():
            raise ValueError(
                f"Перевод невозможен: в целевой группе {self.to_group.number} нет свободных мест."
            )
        self.from_group.expel_student(self.student)
        self.to_group.enroll_student(self.student)
