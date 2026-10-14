from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.operations.flight import Flight

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.infrastructure.baggage_carousel import BaggageCarousel
    from lab3.domain.operations.airline import Airline
    from lab3.domain.operations.flight_plan import FlightPlan


class ArrivalFlight(Flight):
    BAGS_PER_PASSENGER: int = 2

    def __init__(
        self,
        flight_number: str,
        airline: Airline,
        aircraft: Aircraft,
        plan: FlightPlan,
        origin_gate: str = "A1",
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_carousel: BaggageCarousel | None = None
        self.origin_gate = origin_gate
        self.customs_cleared: bool = False

    def assign_carousel(self, carousel: BaggageCarousel) -> None:
        self.assigned_carousel = carousel
        carousel.activate(self)

    def land(self) -> None:
        self._status = "Landed"
        self.aircraft.land()

    def unload_baggage_to_carousel(self) -> int:
        if self.assigned_carousel:
            self.assigned_carousel.activate(self)
        return len(self._passengers) * self.BAGS_PER_PASSENGER
