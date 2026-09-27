import uuid
from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING, Any

from lab3.domain.exceptions import (
    BaggageOverweightException,
    CapacityExceededException,
    FlightDelayedException,
    InvalidTicketException,
)

# Отложенный импорт для статической типизации без циклических зависимостей
if TYPE_CHECKING:
    from lab3.domain.fleet import Aircraft
    from lab3.domain.infrastructure import BaggageCarousel, Gate
    from lab3.domain.people import Passenger


class Baggage:
    """
    Единица багажа пассажира.

    Attributes:
        baggage_id (str): Уникальный RFID-номер багажной бирки.
        weight_kg (float): Вес чемодана в килограммах.
        owner_id (str): Идентификатор пассажира-владельца.
    """
    MAX_STANDARD_WEIGHT = 23.0

    def __init__(self, weight_kg: float, owner_id: str) -> None:
        self.baggage_id = str(uuid.uuid4())
        self.weight_kg = weight_kg
        self.owner_id = owner_id

    def check_weight(self) -> None:
        """Проверяет багаж на перевес."""
        if self.weight_kg > self.MAX_STANDARD_WEIGHT:
            raise BaggageOverweightException(
                f"Перевес: {self.weight_kg} кг. Максимум: {self.MAX_STANDARD_WEIGHT} кг."
            )


class Ticket:
    """
    Маршрутная квитанция (билет) пассажира.

    Attributes:
        ticket_number (str): Уникальный номер билета.
        passenger_id (str): Идентификатор владельца (Person.person_id).
        flight_number (str): Номер рейса (например, "B2 973").
        seat_class (str): Класс обслуживания (Economy, Business, First).
        price (float): Стоимость билета.
    """

    def __init__(
            self, passenger_id: str, flight_number: str, seat_class: str, price: float
    ) -> None:
        self.ticket_number = str(uuid.uuid4())[:8].upper()
        self.passenger_id = passenger_id
        self.flight_number = flight_number
        self.seat_class = seat_class
        self.price = price
        self.is_used = False

    def use_ticket(self) -> None:
        """Помечает билет как использованный после регистрации."""
        if self.is_used:
            raise InvalidTicketException(f"Билет {self.ticket_number} уже был использован.")
        self.is_used = True


class BoardingPass:
    """
    Посадочный талон, выдаваемый после успешной регистрации.

    Attributes:
        pass_id (str): Внутренний номер талона.
        ticket (Ticket): Оригинальный билет.
        seat_number (str): Назначенное место в салоне (например, "12A").
        gate_number (str): Номер гейта для посадки.
    """

    def __init__(self, ticket: Ticket, seat_number: str, gate_number: str) -> None:
        self.pass_id = str(uuid.uuid4())
        self.ticket = ticket
        self.seat_number = seat_number
        self.gate_number = gate_number


class Airline:
    """
    Авиакомпания, осуществляющая перевозки.

    Attributes:
        name (str): Название компании (например, "Belavia").
        iata_code (str): Двухбуквенный код IATA (например, "B2").
    """

    def __init__(self, name: str, iata_code: str) -> None:
        self.airline_id = str(uuid.uuid4())
        self.name = name
        self.iata_code = iata_code
        self._fleet: list['Aircraft'] = []

    def register_aircraft(self, aircraft: 'Aircraft') -> None:
        """Добавляет самолет в парк авиакомпании."""
        self._fleet.append(aircraft)

    @property
    def fleet_size(self) -> int:
        return len(self._fleet)


class FlightPlan:
    """
    Маршрутный лист и расписание конкретного рейса.
    """

    def __init__(self, origin: str, destination: str, scheduled_time: datetime) -> None:
        self.plan_id = str(uuid.uuid4())
        self.origin = origin
        self.destination = destination
        self.scheduled_time = scheduled_time
        self.air_corridor = f"{origin}-{destination}-CORRIDOR-1"


class Flight(ABC):
    """
    Базовый абстрактный класс авиарейса.
    """

    def __init__(
            self, flight_number: str, airline: Airline, aircraft: 'Aircraft', plan: FlightPlan
    ) -> None:
        self.flight_id = str(uuid.uuid4())
        self.flight_number = flight_number
        self.airline = airline
        self.aircraft = aircraft
        self.plan = plan
        self.status = "Scheduled"  # Scheduled, Boarding, InFlight, Landed, Delayed, Cancelled

    def delay(self, reason: str) -> None:
        """Откладывает рейс с указанием причины."""
        if self.status in ["InFlight", "Landed", "Cancelled"]:
            raise ValueError(f"Невозможно отложить рейс в статусе {self.status}.")
        self.status = "Delayed"
        self.delay_reason = reason

    def cancel(self) -> None:
        """Отменяет рейс."""
        self.status = "Cancelled"


class DepartureFlight(Flight):
    """
    Вылетающий рейс. Управляет регистрацией, багажом и посадкой.
    """

    def __init__(
            self, flight_number: str, airline: Airline, aircraft: 'Aircraft', plan: FlightPlan
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_gate: 'Gate | None' = None
        self._manifest: list['Passenger'] = []
        self._cargo_hold: list[Baggage] = []
        self._seat_counter = 1

    def assign_gate(self, gate: 'Gate') -> None:
        """Привязывает гейт к рейсу."""
        self.assigned_gate = gate
        gate.assign_flight(self)

    def check_in_passenger(self, passenger: 'Passenger', ticket: Ticket) -> BoardingPass:
        """
        Регистрирует пассажира на рейс и генерирует посадочный талон.
        """
        if self.status in ["Delayed", "Cancelled"]:
            raise FlightDelayedException(f"Регистрация невозможна: рейс {self.status}.")
        if ticket.flight_number != self.flight_number:
            raise InvalidTicketException("Билет оформлен на другой рейс.")

        ticket.use_ticket()
        self._manifest.append(passenger)

        # Назначает место в формате "1A", "1B" и т.д.
        row = (self._seat_counter // 6) + 1
        letter = chr(65 + (self._seat_counter % 6))
        seat_number = f"{row}{letter}"
        self._seat_counter += 1

        gate_number = self.assigned_gate.number if self.assigned_gate else "TBD"
        return BoardingPass(ticket, seat_number, gate_number)

    def load_baggage(self, baggage: Baggage) -> None:
        """Грузит багаж в трюм самолета."""
        baggage.check_weight()
        self._cargo_hold.append(baggage)

    def start_boarding(self) -> None:
        """Объявляет посадку."""
        if not self.assigned_gate:
            raise ValueError("Гейт не назначен.")
        self.status = "Boarding"
        self.assigned_gate.open_gate()


class ArrivalFlight(Flight):
    """
    Прибывающий рейс. Управляет высадкой и выдачей багажа.
    """

    def __init__(
            self, flight_number: str, airline: Airline, aircraft: 'Aircraft', plan: FlightPlan
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_carousel: 'BaggageCarousel | None' = None
        self.status = "InFlight"

    def assign_carousel(self, carousel: 'BaggageCarousel') -> None:
        """Привязывает карусель для выдачи багажа."""
        self.assigned_carousel = carousel

    def land(self) -> None:
        """Регистрирует приземление рейса."""
        self.status = "Landed"
        self.aircraft.land()
        if self.assigned_carousel:
            self.assigned_carousel.activate(self)


class Schedule:
    """
    Электронное табло рейсов (реестр).
    """

    def __init__(self) -> None:
        self._flights: list[Flight] = []

    def add_flight(self, flight: Flight) -> None:
        self._flights.append(flight)

    def get_departures(self) -> list[DepartureFlight]:
        """Фильтрует и возвращает только вылетающие рейсы."""
        return [f for f in self._flights if isinstance(f, DepartureFlight)]

    def get_arrivals(self) -> list[ArrivalFlight]:
        """Фильтрует и возвращает только прибывающие рейсы."""
        return [f for f in self._flights if isinstance(f, ArrivalFlight)]