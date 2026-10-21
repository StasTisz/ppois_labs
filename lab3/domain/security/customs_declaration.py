"""Модуль пассажирской таможенной декларации."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class CustomsDeclaration:
    """Таможенная декларация на провоз товаров или валюты."""

    def __init__(
        self,
        passenger: Passenger,
        declared_items: list[str],
        cash_amount: float,
        declaration_number: str | None = None,
    ) -> None:
        """Инициализирует экземпляр класса CustomsDeclaration."""
        self.declaration_number = (
            declaration_number or f"DEC-{str(uuid.uuid4())[:8].upper()}"
        )
        self._passenger = passenger
        self._declared_items = list(declared_items)
        self._cash_amount = max(0.0, float(cash_amount))
        self._is_approved = False

    @property
    def declaration_id(self) -> str:
        """Возвращает значение атрибута declaration_id."""
        return self.declaration_number

    @property
    def passenger(self) -> Passenger:
        """Возвращает значение атрибута passenger."""
        return self._passenger

    @property
    def passenger_id(self) -> str:
        """Возвращает значение атрибута passenger_id."""
        return self._passenger.passport_number

    @property
    def declared_items(self) -> list[str]:
        """Возвращает значение атрибута declared_items."""
        return list(self._declared_items)

    @property
    def cash_amount(self) -> float:
        """Возвращает значение атрибута cash_amount."""
        return self._cash_amount

    @property
    def is_approved(self) -> bool:
        """Статус одобрения таможней (только чтение)."""
        return self._is_approved

    def add_item(self, item: str) -> None:
        """Добавляет перемещаемый предмет в таможенную декларацию."""
        if self._is_approved:
            raise ValueError("Нельзя изменять уже одобренную декларацию.")
        self._declared_items.append(item)

    def declare_cash(self, amount: float) -> None:
        """Декларирует сумму перемещаемых наличных денежных средств."""
        if self._is_approved:
            raise ValueError("Нельзя изменять уже одобренную декларацию.")
        if amount < 0:
            raise ValueError("Сумма наличных не может быть отрицательной.")
        self._cash_amount = amount

    def approve(self) -> None:
        """Ставит официальную отметку таможни о прохождении контроля."""
        self._is_approved = True

    def reject(self) -> None:
        """Отклоняет таможенную декларацию из-за несоответствия правилам."""
        self._is_approved = False

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return (
            f"CustomsDeclaration(num={self.declaration_number!r}, passenger={self._passenger!r}, "
            f"cash={self._cash_amount}, items={len(self._declared_items)}, approved={self._is_approved})"
        )
