from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import InvalidTicketException

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.passenger import Passenger


class Ticket:
    def __init__(
            self, passenger: Passenger | str, flight: Flight | str, seat_class: str, price: float
    ) -> None:
        self.ticket_number = str(uuid.uuid4())[:8].upper()
        self.passenger = passenger if not isinstance(passenger, str) else None
        self.passenger_id = getattr(passenger, "person_id", str(passenger))
        self.flight = flight if not isinstance(flight, str) else None
        self.flight_number = getattr(flight, "flight_number", str(flight))
        self.seat_class = seat_class
        self.price = price
        self.is_used = False

    def use_ticket(self) -> None:
        if self.is_used:
            raise InvalidTicketException(f"Билет {self.ticket_number} уже был использован.")
        self.is_used = True
