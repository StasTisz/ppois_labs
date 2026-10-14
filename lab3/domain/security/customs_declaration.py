from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class CustomsDeclaration:
    def __init__(
        self,
        passenger: Passenger | str,
        declared_items: list[str],
        cash_amount: float,
        declaration_number: str | None = None,
    ) -> None:
        self.declaration_number = (
            declaration_number or f"DEC-{str(uuid.uuid4())[:8].upper()}"
        )
        self._passenger = passenger
        self._declared_items = list(declared_items)
        self._cash_amount = max(0.0, float(cash_amount))
        self._is_approved = False

    @property
    def declaration_id(self) -> str:
        return self.declaration_number

    @property
    def passenger(self) -> Passenger | str:
        return self._passenger

    @property
    def passenger_id(self) -> str:
        if hasattr(self._passenger, "passport_number"):
            return self._passenger.passport_number
        if hasattr(self._passenger, "person_id"):
            return self._passenger.person_id
        return str(self._passenger)

    @property
    def declared_items(self) -> list[str]:
        return list(self._declared_items)

    @property
    def cash_amount(self) -> float:
        return self._cash_amount

    @property
    def is_approved(self) -> bool:
        return self._is_approved

    def add_item(self, item: str) -> None:
        if self._is_approved:
            raise ValueError("Нельзя изменять уже одобренную декларацию.")
        self._declared_items.append(item)

    def declare_cash(self, amount: float) -> None:
        if self._is_approved:
            raise ValueError("Нельзя изменять уже одобренную декларацию.")
        if amount < 0:
            raise ValueError("Сумма наличных не может быть отрицательной.")
        self._cash_amount = amount

    def approve(self) -> None:
        self._is_approved = True

    def reject(self) -> None:
        self._is_approved = False

    def __repr__(self) -> str:
        return (
            f"CustomsDeclaration(num={self.declaration_number!r}, passenger={self._passenger!r}, "
            f"cash={self._cash_amount}, items={len(self._declared_items)}, approved={self._is_approved})"
        )
