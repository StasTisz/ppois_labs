from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.person import Person

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.ticket import Ticket


class Passenger(Person):
    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        super().__init__(first_name, last_name, passport_number)
        self.is_boarded = False
        self._tickets: list[Ticket] = []
        self._baggage: list[Baggage] = []

    def buy_ticket(self, ticket: Ticket) -> None:
        self._tickets.append(ticket)

    def add_baggage(self, baggage_item: Baggage) -> None:
        self._baggage.append(baggage_item)

    @property
    def has_tickets(self) -> bool:
        return len(self._tickets) > 0

    @property
    def baggage_count(self) -> int:
        return len(self._baggage)

    def get_tickets(self) -> list[Ticket]:
        return self._tickets.copy()
