from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import GateNotAssignedException

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class Gate:
    def __init__(self, number: str) -> None:
        self.gate_id = str(uuid.uuid4())
        self.number = number
        self.is_open = False
        self.current_flight: Flight | None = None

    def assign_flight(self, flight: Flight) -> None:
        if self.current_flight is not None:
            raise ValueError(f"Гейт {self.number} уже обслуживает другой рейс.")
        self.current_flight = flight

    def open_gate(self) -> None:
        if self.current_flight is None:
            raise GateNotAssignedException(f"Нельзя открыть гейт {self.number}: рейс не назначен.")
        self.is_open = True

    def close_gate(self) -> None:
        self.is_open = False

    def clear_gate(self) -> None:
        self.close_gate()
        self.current_flight = None
