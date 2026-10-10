from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import FlightDelayedException, InvalidTicketException
from lab3.domain.operations.boarding_pass import BoardingPass
from lab3.domain.operations.flight import Flight

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.infrastructure.gate import Gate
    from lab3.domain.operations.airline import Airline
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.operations.flight_plan import FlightPlan
    from lab3.domain.operations.ticket import Ticket
    from lab3.domain.people.passenger import Passenger


class DepartureFlight(Flight):
    def __init__(
            self, flight_number: str, airline: Airline, aircraft: Aircraft, plan: FlightPlan
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_gate: Gate | None = None
        self._manifest: list[Passenger] = []
        self._cargo_hold: list[Baggage] = []
        self._seat_counter = 0

    @property
    def manifest(self) -> list[Passenger]:
        return self._manifest.copy()

    @property
    def cargo_hold(self) -> list[Baggage]:
        return self._cargo_hold.copy()

    def assign_gate(self, gate: Gate) -> None:
        self.assigned_gate = gate
        gate.assign_flight(self)

    def check_in_passenger(self, passenger: Passenger, ticket: Ticket) -> BoardingPass:
        if self.status in ["Delayed", "Cancelled"]:
            raise FlightDelayedException(f"Регистрация невозможна: рейс {self.status}.")
        if ticket.flight_number != self.flight_number:
            raise InvalidTicketException("Билет оформлен на другой рейс.")

        ticket.use_ticket()
        self._manifest.append(passenger)

        row = (self._seat_counter // 6) + 1
        letter = chr(65 + (self._seat_counter % 6))
        seat_number = f"{row}{letter}"
        self._seat_counter += 1

        gate_ref = self.assigned_gate if self.assigned_gate else "TBD"
        return BoardingPass(ticket, seat_number, gate_ref)

    def load_baggage(self, baggage: Baggage) -> None:
        baggage.check_weight()
        self._cargo_hold.append(baggage)

    def start_boarding(self) -> None:
        if not self.assigned_gate:
            raise ValueError("Гейт не назначен.")
        self.status = "Boarding"
        self.assigned_gate.open_gate()
