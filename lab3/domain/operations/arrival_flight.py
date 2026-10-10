from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.operations.flight import Flight

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
    from lab3.domain.operations.airline import Airline
    from lab3.domain.operations.flight_plan import FlightPlan


class ArrivalFlight(Flight):
    def __init__(
            self, flight_number: str, airline: Airline, aircraft: Aircraft, plan: FlightPlan
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_carousel: BaggageCarousel | None = None
        self.status = "InFlight"

    def assign_carousel(self, carousel: BaggageCarousel) -> None:
        self.assigned_carousel = carousel

    def land(self) -> None:
        self.status = "Landed"
        self.aircraft.land()
        if self.assigned_carousel:
            self.assigned_carousel.activate(self)
