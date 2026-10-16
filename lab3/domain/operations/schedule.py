"""Модуль суточного расписания полетов аэропорта."""

from __future__ import annotations

from lab3.domain.operations.arrival_flight import ArrivalFlight
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight import Flight


class Schedule:
    """Электронное табло расписания рейсов (реестр полетов)."""

    def __init__(self, season: str = "Summer", airport_code: str = "MSQ") -> None:
        """Инициализирует экземпляр класса Schedule."""
        self.season = season
        self.airport_code = airport_code
        self._flights: list[Flight] = []

    @property
    def flights(self) -> list[Flight]:
        """Возвращает значение атрибута flights."""
        return list(self._flights)

    def add_flight(self, flight: Flight) -> None:
        """Добавляет рейс в общее расписание."""
        self._flights.append(flight)

    def get_departures(self) -> list[DepartureFlight]:
        """Возвращает список всех вылетающих рейсов."""
        return [
            flight for flight in self._flights if isinstance(flight, DepartureFlight)
        ]

    def get_arrivals(self) -> list[ArrivalFlight]:
        """Возвращает список всех прибывающих рейсов."""
        return [flight for flight in self._flights if isinstance(flight, ArrivalFlight)]

    def find_flight(self, flight_number: str) -> Flight | None:
        """Выполняет поиск авиарейса в расписании по номеру рейса."""
        for flight in self._flights:
            if flight.flight_number == flight_number:
                return flight
        return None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Schedule(code={self.airport_code!r}, season={self.season!r}, total_flights={len(self._flights)})"
