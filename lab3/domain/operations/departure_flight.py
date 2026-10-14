from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import (
    BoardingClosedException,
    FlightDelayedException,
    GateNotAssignedException,
    InvalidTicketException,
    MaintenanceRequiredException,
    NoAvailableCrewException,
)
from lab3.domain.operations.boarding_pass import BoardingPass
from lab3.domain.operations.flight import Flight
from lab3.domain.people.pilot import Pilot

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
        self,
        flight_number: str,
        airline: Airline,
        aircraft: Aircraft,
        plan: FlightPlan,
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_gate: Gate | None = None
        self._manifest: list[Passenger] = []
        self._cargo_hold: list[Baggage] = []
        self._seat_counter = 0

    @property
    def manifest(self) -> list[Passenger]:
        return list(self._manifest)

    @property
    def cargo_hold(self) -> list[Baggage]:
        return list(self._cargo_hold)

    def assign_gate(self, gate: Gate) -> None:
        self.assigned_gate = gate
        super().assign_gate(gate)

    def check_in_passenger(self, passenger: Passenger, ticket: Ticket) -> BoardingPass:
        if self.status in ["Delayed", "Cancelled"]:
            raise FlightDelayedException(f"Регистрация невозможна: рейс {self.status}.")
        if ticket.flight_number != self.flight_number:
            raise InvalidTicketException("Билет оформлен на другой рейс.")

        ticket.use_ticket()
        if passenger not in self._manifest:
            self._manifest.append(passenger)

        row = (self._seat_counter // 6) + 1
        letter = chr(65 + (self._seat_counter % 6))
        seat_number = f"{row}{letter}"
        self._seat_counter += 1

        return BoardingPass(ticket, seat_number, gate=self.assigned_gate)

    def board_passenger(
        self, passenger: Passenger, boarding_pass: BoardingPass
    ) -> None:
        if not self.assigned_gate or not self.assigned_gate.is_open:
            raise BoardingClosedException(
                f"Посадка на рейс {self.flight_number} окончена или гейт закрыт."
            )
        boarding_pass.mark_boarded()
        passenger.board()
        if passenger not in self._passengers:
            self._passengers.append(passenger)

    def load_baggage(self, baggage: Baggage) -> None:
        baggage.check_weight()
        self._cargo_hold.append(baggage)

    def start_boarding(self) -> None:
        if not self.assigned_gate:
            raise GateNotAssignedException("Гейт не назначен.")
        self._status = "Boarding"
        self.assigned_gate.open_gate()

    def close_boarding(self) -> None:
        if self.assigned_gate:
            self.assigned_gate.close_gate()
        self._status = "BoardingClosed"

    def authorize_takeoff(self) -> None:
        if getattr(self.aircraft, "requires_maintenance", False):
            raise MaintenanceRequiredException(
                f"Вылет запрещен: борт {self.aircraft.tail_number} требует прохождения ТО."
            )
        has_captain = any(isinstance(c, Pilot) and c.is_captain for c in self._crew)
        if not self._crew or not has_captain:
            raise NoAvailableCrewException(
                f"Вылет запрещен: для рейса {self.flight_number} не укомплектован экипаж с КВС."
            )
        self._status = "Departed"
        return True
