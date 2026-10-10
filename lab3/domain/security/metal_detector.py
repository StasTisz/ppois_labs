from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.security.scanner import Scanner

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger


class MetalDetector(Scanner):
    def scan(self, target: Passenger | Baggage | None) -> bool:
        if not self.is_active:
            raise ValueError(f"Детектор {self.model} выключен.")
        return True
