from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.operations.ticket import Ticket

if TYPE_CHECKING:
    from lab3.domain.infrastructure.gate import Gate


class BoardingPass:
    def __init__(
        self, ticket: Ticket, seat_number: str, gate: Gate | str = "TBD"
    ) -> None:
        self.pass_id = str(uuid.uuid4())
        self.ticket = ticket
        self.seat_number = seat_number
        self.gate: Gate | None = gate if not isinstance(gate, str) else None
        self._gate_str_fallback = gate if isinstance(gate, str) else None
        self._is_boarded = False

    @property
    def gate_number(self) -> str:
        if self.gate is not None:
            return self.gate.number
        return self._gate_str_fallback or "TBD"

    @property
    def is_boarded(self) -> bool:
        return self._is_boarded

    def mark_boarded(self) -> None:
        self._is_boarded = True

    def verify_gate(self, current_gate: Gate) -> bool:
        if self.gate is None:
            return False
        return self.gate == current_gate

    def change_seat(self, new_seat: str) -> None:
        if self._is_boarded:
            raise ValueError("Нельзя изменить место: посадка уже завершена.")
        self.seat_number = new_seat

    def assign_gate(self, gate: Gate) -> None:
        self.gate = gate
        self._gate_str_fallback = None

    def get_summary(self) -> str:
        return (
            f"Pass #{self.pass_id[:8]}: Seat {self.seat_number}, Gate {self.gate_number}, "
            f"Boarded: {self._is_boarded}"
        )

    def __repr__(self) -> str:
        return f"BoardingPass(ticket={self.ticket!r}, seat={self.seat_number!r}, gate={self.gate_number!r})"
