from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import SecurityCheckFailedException
from lab3.domain.security.customs_declaration import CustomsDeclaration

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class CustomsControl:
    MAX_CASH_ALLOWED_USD = 10000.0

    def __init__(self, control_number: int = 1) -> None:
        self.control_number = control_number
        self._inspections_count = 0

    @property
    def control_id(self) -> str:
        return f"CC-{self.control_number}"

    @property
    def inspections_count(self) -> int:
        return self._inspections_count

    def inspect_declaration(self, declaration: CustomsDeclaration) -> None:
        if declaration.cash_amount > self.MAX_CASH_ALLOWED_USD:
            raise SecurityCheckFailedException(
                f"Сумма {declaration.cash_amount}$ превышает лимит вывоза "
                f"без дополнительных разрешений ({self.MAX_CASH_ALLOWED_USD}$)."
            )
        declaration.approve()
        self._inspections_count += 1

    def confiscate_excess(self, declaration: CustomsDeclaration) -> float:
        if declaration.cash_amount <= self.MAX_CASH_ALLOWED_USD:
            return 0.0
        excess = declaration.cash_amount - self.MAX_CASH_ALLOWED_USD
        declaration.declare_cash(self.MAX_CASH_ALLOWED_USD)
        return excess

    def stamp_passport(self, passenger: Passenger) -> str:
        return f"Таможенный контроль пройден пассажиром {passenger.passport_number}"

    def __repr__(self) -> str:
        return f"CustomsControl(number={self.control_number}, inspections={self._inspections_count})"
