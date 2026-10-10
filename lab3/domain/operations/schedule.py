from __future__ import annotations

from lab3.domain.operations.arrival_flight import ArrivalFlight
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight import Flight


class Schedule:
    def __init__(self) -> None:
        self._flights: list[Flight] = []

    def add_flight(self, flight: Flight) -> None:
        self._flights.append(flight)

    def get_departures(self) -> list[DepartureFlight]:
        return [f for f in self._flights if isinstance(f, DepartureFlight)]

    def get_arrivals(self) -> list[ArrivalFlight]:
        return [f for f in self._flights if isinstance(f, ArrivalFlight)]
