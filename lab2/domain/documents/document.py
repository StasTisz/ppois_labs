from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from lab2.domain.exceptions import DocumentNotSignedException

if TYPE_CHECKING:
    from lab2.domain.people.dean import Dean


class Document:
    def __init__(self, title: str, registration_number: str = "") -> None:
        self.registration_number = (
            registration_number
            or f"DOC-{abs(hash((title, datetime.now(UTC).isoformat()))) % 1000000:06d}"
        )
        self.title = title
        self.created_at = datetime.now(UTC)
        self._is_signed = False
        self._signer: Dean | None = None

    @property
    def is_signed(self) -> bool:
        return self._is_signed

    @property
    def signer(self) -> Dean | None:
        return self._signer

    def sign(self, dean: Dean) -> None:
        if self._is_signed:
            raise ValueError(f"Документ '{self.title}' уже подписан.")
        self._is_signed = True
        self._signer = dean

    def _ensure_signed(self) -> None:
        if not self._is_signed:
            raise DocumentNotSignedException(
                f"Операция отклонена: документ '{self.title}' не подписан."
            )

    def verify_signature(self) -> bool:
        return self._is_signed and self._signer is not None

    @property
    def status(self) -> str:
        return "Подписан" if self._is_signed else "Проект"

    def cancel_document(self, reason: str) -> None:
        self._ensure_signed()
        self._is_signed = False
        self._signer = None
        self.cancellation_reason = reason
        self.title = f"[АННУЛИРОВАН: {reason}] {self.title}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(reg={self.registration_number!r}, title={self.title!r}, signed={self._is_signed})"
