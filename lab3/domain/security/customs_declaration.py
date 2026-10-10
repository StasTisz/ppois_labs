from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class CustomsDeclaration:
    def __init__(self, passenger: Passenger | str, declared_items: list[str], cash_amount: float) -> None:
        self.declaration_id = str(uuid.uuid4())
        self.passenger = passenger if not isinstance(passenger, str) else None
        self.passenger_id = getattr(passenger, "person_id", str(passenger))
        self.declared_items = declared_items
        self.cash_amount = cash_amount
        self._is_approved = False

    @property
    def is_approved(self) -> bool:
        return self._is_approved

    def approve(self) -> None:
        self._is_approved = True
