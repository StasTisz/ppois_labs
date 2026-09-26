import uuid
from datetime import datetime, timezone

from lab2.domain.exceptions import ExpulsionDeniedException
from lab2.domain.people import Dean, Student
from lab2.domain.structure import AcademicGroup


class Document:
    """
    Базовый класс для любого официального документа деканата.

    Attributes:
        title (str): Заголовок/название документа.
        document_id (str): Уникальный внутренний номер (UUID).
        created_at (datetime): Дата и время создания (в UTC).
        is_signed (bool): Статус подписания.
        signer (Dean | None): Уполномоченное лицо, подписавшее документ.
    """

    def __init__(self, title: str) -> None:
        self.document_id = str(uuid.uuid4())
        self.title = title
        self.created_at = datetime.now(timezone.utc)
        self.is_signed = False
        self.signer: Dean | None = None

    def sign(self, dean: Dean) -> None:
        """
        Утверждает документ уполномоченным лицом.

        Args:
            dean (Dean): Декан, подписывающий документ.

        Raises:
            ValueError: Если документ уже был подписан ранее.
        """
        if self.is_signed:
            raise ValueError(f"Документ '{self.title}' уже подписан.")
        self.is_signed = True
        self.signer = dean

    def _ensure_signed(self) -> None:
        """
        Внутренний валидатор: проверяет, подписан ли документ перед его исполнением.

        Raises:
            ValueError: Если документ еще в статусе проекта.
        """
        if not self.is_signed:
            raise ValueError(f"Операция отклонена: документ '{self.title}' не подписан.")

    @property
    def status(self) -> str:
        """Агрегация: возвращает текстовый статус документа."""
        return "Подписан" if self.is_signed else "Проект"

    def cancel_document(self, reason: str) -> None:
        """
        Аннулирует уже подписанный документ (например, при обнаружении ошибки).

        Args:
            reason (str): Причина аннулирования.

        Raises:
            ValueError: Если документ не был подписан.
        """
        self._ensure_signed()
        self.is_signed = False
        self.signer = None
        self.title = f"[АННУЛИРОВАН: {reason}] {self.title}"


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

        # Легитимные причины: "академическая неуспеваемость" или заявление "по собственному"
        reason_lower = self.reason.lower()
        has_academic_ground = "академическ" in reason_lower or "неуспеваемост" in reason_lower
        is_voluntary = "по собственному" in reason_lower

        # Если нет финансовых долгов, нет академических оснований и нет личного заявления — отчислять нельзя
        if self.student.financial_debt == 0.0 and not has_academic_ground and not is_voluntary:
            raise ExpulsionDeniedException(f"Нет оснований для отчисления студента {self.student.full_name}")

        self.student.expel()


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


class TransferOrder(Document):
    """
    Приказ о переводе студента из одной академической группы в другую.

    Attributes:
        student (Student): Переводимый студент.
        from_group (AcademicGroup): Исходная группа.
        to_group (AcademicGroup): Целевая группа.
    """

    def __init__(self, student: Student, from_group: AcademicGroup, to_group: AcademicGroup) -> None:
        super().__init__(f"Приказ о переводе: {student.full_name}")
        self.student = student
        self.from_group = from_group
        self.to_group = to_group

    def execute(self) -> None:
        """Осуществляет физическое перемещение студента между группами."""
        self._ensure_signed()
        self.from_group.expel_student(self.student)
        self.to_group.enroll_student(self.student)


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


class AcademicLeaveOrder(Document):
    """
    Приказ о предоставлении академического отпуска.

    Attributes:
        student (Student): Студент, уходящий в отпуск.
        reason (str): Причина отпуска.
        duration_months (int): Длительность в месяцах.
    """

    def __init__(self, student: Student, reason: str, duration_months: int) -> None:
        super().__init__(f"Академический отпуск: {student.full_name}")
        self.student = student
        self.reason = reason
        self.duration_months = duration_months

    def execute(self) -> None:
        """Замораживает статус студента (отключает стипендию и переводит в неактивный статус)."""
        self._ensure_signed()
        self.student.is_active = False
        self.student.has_scholarship = False


class ReprimandOrder(Document):
    """
    Приказ о выговоре за нарушение устава вуза или правил общежития.

    Attributes:
        student (Student): Студент, получающий выговор.
        reason (str): Причина наказания.
        is_strict (bool): Является ли выговор строгим (с лишением стипендии).
    """

    def __init__(self, student: Student, reason: str, is_strict: bool = False) -> None:
        super().__init__(f"Приказ о выговоре: {student.full_name}")
        self.student = student
        self.reason = reason
        self.is_strict = is_strict

    def execute(self) -> None:
        """Применяет санкции к студенту (лишение стипендии при строгом выговоре)."""
        self._ensure_signed()

        # Бизнес-правило: строгий выговор автоматически лишает стипендии
        if self.is_strict and self.student.has_scholarship:
            self.student.has_scholarship = False