from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab2.domain.people.dean import Dean


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
