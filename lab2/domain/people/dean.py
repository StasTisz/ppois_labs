"""Модуль декана факультета."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab2.domain.people.employee import Employee

if TYPE_CHECKING:
    from lab2.domain.documents.document import Document


class Dean(Employee):
    """Декан факультета. Подписывает приказы и руководит факультетом."""

    DEFAULT_DEGREE = "К.т.н."
    DEFAULT_POSITION = "Декан"

    def __init__(
        self,
        first_name: str,
        last_name: str,
        middle_name: str = "",
        degree: str = DEFAULT_DEGREE,
        passport_number: str = "",
    ) -> None:
        """Инициализирует экземпляр класса Dean."""
        super().__init__(
            first_name,
            last_name,
            middle_name,
            position=self.DEFAULT_POSITION,
            passport_number=passport_number,
        )
        self.degree = degree
        self.faculty_name = "ФИТиУ"
        self.cabinet_number = "215-1"
        self._signed_orders_count = 0

    @property
    def signed_orders_count(self) -> int:
        """Возвращает значение атрибута signed_orders_count."""
        return self._signed_orders_count

    def sign_order(self, order: Document) -> str:
        """Подписывает приказ по факультету."""
        self._signed_orders_count += 1
        order.sign(self)
        return f"ПРИКАЗ УТВЕРЖДЕН: {order.title} | Подписант: декан {self.full_name}"

    def issue_instruction(self, instruction_text: str) -> str:
        """Издает распоряжение декана факультета."""
        if not instruction_text.strip():
            raise ValueError("Текст распоряжения не может быть пустым.")
        return f"РАСПОРЯЖЕНИЕ ДЕКАНА ({self.full_name}): {instruction_text}"

    def veto_order(self, order: Document, reason: str) -> None:
        """Накладывает вето на проект административного приказа."""
        if not reason.strip():
            raise ValueError("Причина вето должна быть указана.")
        order.cancel_document(f"Вето декана {self.full_name}: {reason}")
