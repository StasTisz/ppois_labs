from datetime import UTC, datetime

from lab2.domain.documents.document import Document
from lab2.domain.people.student import Student


class ReprimandOrder(Document):
    def __init__(
        self,
        student: Student,
        reason: str,
        is_strict: bool = False,
        registration_number: str = "",
    ) -> None:
        super().__init__(
            f"Приказ о выговоре: {student.full_name}",
            registration_number=registration_number,
        )
        self.student = student
        self.reason = reason
        self.is_strict = is_strict
        self.issued_date = datetime.now(UTC)

    def execute(self) -> None:
        self._ensure_signed()
        if self.is_strict and self.student.has_scholarship:
            self.student.revoke_scholarship()

    def appeal(self, grounds: str) -> None:
        if not grounds.strip():
            raise ValueError(
                "Основание для обжалования выговора должно быть заполнено."
            )
        self.cancel_document(f"Апелляция удовлетворена: {grounds}")
