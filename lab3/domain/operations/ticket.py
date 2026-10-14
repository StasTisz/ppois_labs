from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import InvalidTicketException

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight
    from lab3.domain.people.passenger import Passenger


class Ticket:
    _ticket_counter: int = 100000

    def __init__(
        self,
        passenger: Passenger,
        flight: Flight,
        seat_class: str,
        price: float,
        ticket_number: str | None = None,
    ) -> None:
        Ticket._ticket_counter += 1
        self.ticket_number = ticket_number or f"TK-{Ticket._ticket_counter}"
        self._passenger = passenger
        self._flight = flight
        self._seat_class = seat_class
        self._price = max(0.0, float(price))
        self._is_used = False

    @property
    def passenger(self) -> Passenger:
        return self._passenger

    @property
    def flight(self) -> Flight:
        return self._flight

    @property
    def flight_number(self) -> str:
        return self._flight.flight_number

    @property
    def seat_class(self) -> str:
        return self._seat_class

    @property
    def price(self) -> float:
        return self._price

    @property
    def is_used(self) -> bool:
        return self._is_used

    def use_ticket(self) -> None:
        if self._is_used:
            raise InvalidTicketException(
                f"Билет {self.ticket_number} уже был использован."
            )
        self._is_used = True

    def cancel_ticket(self) -> None:
        if self._is_used:
            raise InvalidTicketException(
                f"Нельзя отменить уже использованный билет {self.ticket_number}."
            )
        self._price = 0.0

    def upgrade_class(self, new_class: str, additional_fee: float = 0.0) -> None:
        if self._is_used:
            raise InvalidTicketException(
                f"Нельзя повысить класс обслуживания по использованному билету {self.ticket_number}."
            )
        self._seat_class = new_class
        self._price += max(0.0, float(additional_fee))

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Ticket):
            return False
        return self.ticket_number == other.ticket_number

    def __repr__(self) -> str:
        return f"Ticket(number={self.ticket_number!r}, flight={self.flight_number!r}, passenger={self._passenger.full_name!r})"
