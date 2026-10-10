from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.operations.ticket import Ticket

if TYPE_CHECKING:
    from lab3.domain.infrastructure.gate import Gate


class BoardingPass:
    def __init__(self, ticket: Ticket, seat_number: str, gate: Gate | str = "TBD") -> None:
        self.pass_id = str(uuid.uuid4())
        self.ticket = ticket
        self.seat_number = seat_number
        self.gate = gate if not isinstance(gate, str) else None
        self.gate_number = getattr(gate, "number", str(gate))
