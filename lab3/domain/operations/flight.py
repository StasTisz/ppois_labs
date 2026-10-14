from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.infrastructure.gate import Gate
    from lab3.domain.infrastructure.runway import Runway
    from lab3.domain.operations.airline import Airline
    from lab3.domain.operations.flight_plan import FlightPlan
    from lab3.domain.people.crew_member import CrewMember
    from lab3.domain.people.passenger import Passenger


class Flight(ABC):
    def __init__(
        self,
        flight_number: str,
        airline: Airline,
        aircraft: Aircraft,
        plan: FlightPlan,
    ) -> None:
        self.flight_number = flight_number
        self.airline = airline
        self.aircraft = aircraft
        self.plan = plan
        self._status = "Scheduled"
        self._delay_reason: str | None = None
        self._crew: list[CrewMember] = []
        self._passengers: list[Passenger] = []
        self.gate: Gate | None = None
        self.runway: Runway | None = None

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, new_status: str) -> None:
        self._status = new_status

    @property
    def delay_reason(self) -> str | None:
        return self._delay_reason

    @property
    def crew(self) -> list[CrewMember]:
        return list(self._crew)

    @property
    def passengers(self) -> list[Passenger]:
        return list(self._passengers)

    def assign_crew(self, crew_member: CrewMember) -> None:
        if crew_member not in self._crew:
            self._crew.append(crew_member)

    def assign_gate(self, gate: Gate | None) -> None:
        self.gate = gate
        if gate and hasattr(gate, "assign_flight"):
            gate.assign_flight(self)

    def assign_runway(self, runway: Runway | None) -> None:
        self.runway = runway

    def delay(self, reason: str) -> None:
        if self._status in ["InFlight", "Landed", "Cancelled"]:
            raise ValueError(f"Невозможно отложить рейс в статусе {self._status}.")
        self._status = "Delayed"
        self._delay_reason = reason

    def cancel(self) -> None:
        self._status = "Cancelled"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(num={self.flight_number!r}, status={self._status!r}, plane={self.aircraft.tail_number!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Flight):
            return NotImplemented
        return self.flight_number == other.flight_number

    def __hash__(self) -> int:
        return hash(self.flight_number)
