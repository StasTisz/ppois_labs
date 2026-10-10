from __future__ import annotations

import uuid
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.operations.airline import Airline
    from lab3.domain.operations.flight_plan import FlightPlan


class Flight(ABC):
    def __init__(
            self, flight_number: str, airline: Airline, aircraft: Aircraft, plan: FlightPlan
    ) -> None:
        self.flight_id = str(uuid.uuid4())
        self.flight_number = flight_number
        self.airline = airline
        self.aircraft = aircraft
        self.plan = plan
        self.status = "Scheduled"
        self.delay_reason: str | None = None

    def delay(self, reason: str) -> None:
        if self.status in ["InFlight", "Landed", "Cancelled"]:
            raise ValueError(f"Невозможно отложить рейс в статусе {self.status}.")
        self.status = "Delayed"
        self.delay_reason = reason

    def cancel(self) -> None:
        self.status = "Cancelled"
