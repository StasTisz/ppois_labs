"""Модуль приказа о дисциплинарном взыскании (выговоре)."""

from datetime import UTC, datetime

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ReprimandOrder(Document):
    """Приказ о выговоре за нарушение устава вуза или правил общежития."""

    def __init__(
        self,
        student: Student,
        reason: str,
        is_strict: bool = False,
        registration_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса ReprimandOrder."""
        super().__init__(
            f"Приказ о выговоре: {student.full_name}",
            registration_number=registration_number,
        )
        self.student = student
        self.reason = reason
        self.is_strict = is_strict
        self.issued_date = datetime.now(UTC)

    def execute(self) -> None:
        """Применяет санкции к студенту (лишение стипендии при строгом выговоре)."""
        self._ensure_signed()
        if self.is_strict and self.student.has_scholarship:
            self.student.revoke_scholarship()

    def appeal(self, grounds: str) -> None:
        """Подает апелляцию на вынесенное дисциплинарное взыскание (выговор)."""
        if not grounds.strip():
            raise ValueError(
                "Основание для обжалования выговора должно быть заполнено."
            )
        self.cancel_document(f"Апелляция удовлетворена: {grounds}")
