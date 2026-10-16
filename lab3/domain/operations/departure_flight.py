"""Модуль вылетающего авиарейса."""

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
    """Вылетающий рейс. Управляет процессом регистрации, багажом и посадкой."""

    SEATS_PER_ROW: int = 6
    ASCII_OFFSET_A: int = 65

    def __init__(
        self,
        flight_number: str,
        airline: Airline,
        aircraft: Aircraft,
        plan: FlightPlan,
    ) -> None:
        """Инициализирует экземпляр класса DepartureFlight."""
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_gate: Gate | None = None
        self._manifest: list[Passenger] = []
        self._cargo_hold: list[Baggage] = []
        self._seat_counter = 0

    @property
    def manifest(self) -> list[Passenger]:
        """Безопасная копия списка зарегистрированных пассажиров."""
        return list(self._manifest)

    @property
    def cargo_hold(self) -> list[Baggage]:
        """Безопасная копия списка загруженного багажа."""
        return list(self._cargo_hold)

    def assign_gate(self, gate: Gate | None) -> None:
        """Привязывает инфраструктурный гейт к текущему рейсу."""
        self.assigned_gate = gate
        super().assign_gate(gate)

    def check_in_passenger(self, passenger: Passenger, ticket: Ticket) -> BoardingPass:
        """Регистрирует пассажира на рейс, гасит билет и генерирует посадочный талон."""
        if self.status in ["Delayed", "Cancelled"]:
            raise FlightDelayedException(f"Регистрация невозможна: рейс {self.status}.")
        if ticket.flight_number != self.flight_number:
            raise InvalidTicketException("Билет оформлен на другой рейс.")

        ticket.use_ticket()
        if passenger not in self._manifest:
            self._manifest.append(passenger)

        row = (self._seat_counter // self.SEATS_PER_ROW) + 1
        letter = chr(self.ASCII_OFFSET_A + (self._seat_counter % self.SEATS_PER_ROW))
        seat_number = f"{row}{letter}"
        self._seat_counter += 1

        return BoardingPass(ticket, seat_number, gate=self.assigned_gate)

    def board_passenger(
        self, passenger: Passenger, boarding_pass: BoardingPass
    ) -> None:
        """Регистрирует посадку пассажира по посадочному талону."""
        if not self.assigned_gate or not self.assigned_gate.is_open:
            raise BoardingClosedException(
                f"Посадка на рейс {self.flight_number} окончена или гейт закрыт."
            )
        boarding_pass.mark_boarded()
        passenger.board()
        if passenger not in self._passengers:
            self._passengers.append(passenger)

    def load_baggage(self, baggage: Baggage) -> None:
        """Грузит проверенный багаж в трюм самолета."""
        baggage.check_weight()
        self._cargo_hold.append(baggage)

    def start_boarding(self) -> None:
        """Объявляет посадку и открывает привязанный гейт."""
        if not self.assigned_gate:
            raise GateNotAssignedException("Гейт не назначен.")
        self._status = "Boarding"
        self.assigned_gate.open_gate()

    def close_boarding(self) -> None:
        """Закрывает выход на посадку перед вылетом воздушного судна."""
        if self.assigned_gate:
            self.assigned_gate.close_gate()
        self._status = "BoardingClosed"

    def authorize_takeoff(self) -> bool:
        """Выдает разрешение на взлет рейса при выполнении всех предполетных условий."""
        if getattr(self.aircraft, "requires_maintenance", False):
            raise MaintenanceRequiredException(
                f"Вылет запрещен: борт {self.aircraft.tail_number} требует прохождения ТО."
            )
        has_captain = any(
            isinstance(member, Pilot) and member.is_captain for member in self._crew
        )
        if not self._crew or not has_captain:
            raise NoAvailableCrewException(
                f"Вылет запрещен: для рейса {self.flight_number} не укомплектован экипаж с КВС."
            )
        self._status = "Departed"
        return True
