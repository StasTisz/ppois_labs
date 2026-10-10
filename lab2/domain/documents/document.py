from __future__ import annotations

import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING

from lab2.domain.exceptions import DocumentNotSignedException

if TYPE_CHECKING:
    from lab2.domain.people.dean import Dean


class Document:
    def __init__(self, title: str) -> None:
        self.document_id = str(uuid.uuid4())
        self.title = title
        self.created_at = datetime.now(UTC)
        self.is_signed = False
        self.signer: Dean | None = None

    def sign(self, dean: Dean) -> None:
        if self.is_signed:
            raise ValueError(f"Документ '{self.title}' уже подписан.")
        self.is_signed = True
        self.signer = dean

    def _ensure_signed(self) -> None:
        if not self.is_signed:
            raise DocumentNotSignedException(f"Операция отклонена: документ '{self.title}' не подписан.")

    @property
    def status(self) -> str:
        return "Подписан" if self.is_signed else "Проект"

    def cancel_document(self, reason: str) -> None:
        self._ensure_signed()
        self.is_signed = False
        self.signer = None
        self.title = f"[АННУЛИРОВАН: {reason}] {self.title}"
