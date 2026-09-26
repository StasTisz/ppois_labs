import uuid
from datetime import datetime

from lab2.domain.exceptions import ExpulsionDeniedException
from lab2.domain.people import Dean, Student
from lab2.domain.structure import AcademicGroup


class Document:
    """Базовый класс для любого официального документа деканата."""

    def __init__(self, title: str):
        self.document_id = str(uuid.uuid4())
        self.title = title
        self.created_at = datetime.now()
        self.is_signed = False
        self.signer: Dean | None = None

    def sign(self, dean: Dean):
        """Поведение: подписание документа уполномоченным лицом."""
        if self.is_signed:
            raise ValueError(f"Документ '{self.title}' уже подписан.")
        self.is_signed = True
        self.signer = dean

    @property
    def status(self) -> str:
        return "Подписан" if self.is_signed else "Проект"

    def cancel_document(self, reason: str):
        """Поведение: аннулирование уже подписанного документа (например, при ошибке)."""
        if not self.is_signed:
            raise ValueError("Нельзя аннулировать неподписанный проект.")
        self.is_signed = False
        self.signer = None
        self.title = f"[АННУЛИРОВАН: {reason}] {self.title}"


class ExpulsionOrder(Document):
    """Приказ об отчислении студента."""

    def __init__(self, student: Student, reason: str):
        super().__init__(f"Приказ об отчислении: {student.full_name}")
        self.student = student
        self.reason = reason

    def execute(self):
        """Поведение: применение приказа (меняет статус студента)."""
        if not self.is_signed:
            raise ValueError("Нельзя пустить в дело неподписанный проект приказа.")

        # Легитимные причины: неуспеваемость или заявление по собственному
        reason_lower = self.reason.lower()
        has_academic_ground = "академическ" in reason_lower or "неуспеваемост" in reason_lower
        is_voluntary = "по собственному" in reason_lower

        # Если нет финансовых долгов, нет академических оснований и нет личного заявления — отчислять нельзя
        if self.student.financial_debt == 0.0 and not has_academic_ground and not is_voluntary:
            raise ExpulsionDeniedException(f"Нет оснований для отчисления студента {self.student.full_name}")

        self.student.expel()


class AcademicCertificate(Document):
    """Справка об обучении (например, по месту требования)."""

    def __init__(self, student: Student, destination: str):
        super().__init__(f"Справка об обучении: {student.full_name}")
        self.student = student
        self.destination = destination


class TransferOrder(Document):
    """Приказ о переводе студента из одной группы в другую."""

    def __init__(self, student: Student, from_group: AcademicGroup, to_group: AcademicGroup):
        super().__init__(f"Приказ о переводе: {student.full_name}")
        self.student = student
        self.from_group = from_group
        self.to_group = to_group

    def execute(self):
        """Поведение: физическое перемещение студента между группами."""
        if not self.is_signed:
            raise ValueError("Нельзя исполнить неподписанный приказ о переводе.")

        self.from_group.expel_student(self.student)
        self.to_group.enroll_student(self.student)


class ScholarshipOrder(Document):
    """Массовый приказ о назначении стипендии по итогам сессии."""

    def __init__(self, students: list[Student]):
        super().__init__(f"Приказ о стипендии ({len(students)} чел.)")
        self.students = students

    def execute(self):
        """Поведение: массовое начисление стипендии."""
        if not self.is_signed:
            raise ValueError("Нельзя исполнить неподписанный приказ.")

        for student in self.students:
            student.grant_scholarship()


class AcademicLeaveOrder(Document):
    """Приказ о предоставлении академического отпуска."""

    def __init__(self, student: Student, reason: str, duration_months: int):
        super().__init__(f"Академический отпуск: {student.full_name}")
        self.student = student
        self.reason = reason
        self.duration_months = duration_months

    def execute(self):
        """Поведение: заморозка статуса студента."""
        if not self.is_signed:
            raise ValueError("Нельзя исполнить неподписанный приказ.")

        self.student.is_active = False
        self.student.has_scholarship = False


class ReprimandOrder(Document):
    """Приказ о выговоре за нарушение устава вуза или общежития."""

    def __init__(self, student: Student, reason: str, is_strict: bool = False):
        super().__init__(f"Приказ о выговоре: {student.full_name}")
        self.student = student
        self.reason = reason
        self.is_strict = is_strict  # Строгий выговор с занесением

    def execute(self):
        """Поведение: применение санкций."""
        if not self.is_signed:
            raise ValueError("Нельзя пустить в дело неподписанный проект приказа.")

        # Бизнес-правило: строгий выговор автоматически лишает стипендии
        if self.is_strict and self.student.has_scholarship:
            self.student.has_scholarship = False