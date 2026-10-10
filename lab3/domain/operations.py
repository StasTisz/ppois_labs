"""
Модуль операционной деятельности аэропорта.

Отвечает за логику управления рейсами, билетами, багажом и расписанием.
Связывает воедино инфраструктуру (гейты, карусели), флот (самолеты) и людей (пассажиров).
Обеспечивает транзакционность при регистрации на рейс и посадке.
"""

from __future__ import annotations

import uuid
from abc import ABC
from datetime import datetime
from typing import TYPE_CHECKING

from lab3.domain.exceptions import (
    BaggageOverweightException,
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
        weight_kg (float): Фактический вес чемодана в килограммах.
        owner_id (str): Идентификатор пассажира-владельца.
    """
    MAX_STANDARD_WEIGHT = 23.0

    def __init__(self, weight_kg: float, owner_id: str) -> None:
        self.baggage_id = str(uuid.uuid4())
        self.weight_kg = weight_kg
        self.owner_id = owner_id

    def check_weight(self) -> None:
        """
        Проверяет багаж на соответствие нормам провоза.

        Raises:
            BaggageOverweightException: Если вес превышает допустимый лимит.
        """
        if self.weight_kg > self.MAX_STANDARD_WEIGHT:
            raise BaggageOverweightException(
                f"Перевес: {self.weight_kg} кг. Максимум: {self.MAX_STANDARD_WEIGHT} кг."
            )


class Ticket:
    """
    Маршрутная квитанция (электронный билет) пассажира.

    Attributes:
        ticket_number (str): Уникальный 8-значный буквенно-цифровой номер билета.
        passenger_id (str): Идентификатор владельца (связь с Person.person_id).
        flight_number (str): Номер рейса (например, "B2-973").
        seat_class (str): Класс обслуживания (Economy, Business, First).
        price (float): Стоимость приобретенного билета.
        is_used (bool): Флаг гашения билета после успешной регистрации.
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
        """
        Помечает билет как использованный (гасит его).

        Raises:
            InvalidTicketException: Если билет уже был погашен ранее.
        """
        if self.is_used:
            raise InvalidTicketException(f"Билет {self.ticket_number} уже был использован.")
        self.is_used = True


class BoardingPass:
    """
    Посадочный талон, выдаваемый после успешной регистрации и сдачи багажа.

    Attributes:
        pass_id (str): Внутренний номер посадочного талона.
        ticket (Ticket): Ссылка на оригинальный билет.
        seat_number (str): Назначенное место в салоне (например, "12A").
        gate_number (str): Номер гейта для посадки ("TBD", если еще не назначен).
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
        self._fleet: list[Aircraft] = []

    def register_aircraft(self, aircraft: Aircraft) -> None:
        """Регистрирует воздушное судно в парке авиакомпании."""
        self._fleet.append(aircraft)

    @property
    def fleet_size(self) -> int:
        """Текущее количество самолетов во флоте компании."""
        return len(self._fleet)

    def get_fleet(self) -> list[Aircraft]:
        """Возвращает копию списка флота для безопасного перебора."""
        return self._fleet.copy()


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

    Attributes:
        flight_number (str): Уникальный номер рейса.
        airline (Airline): Компания-оператор.
        aircraft (Aircraft): Воздушное судно, выполняющее рейс.
        plan (FlightPlan): План полета.
        status (str): Текущий статус рейса (Scheduled, Boarding, InFlight, Landed, Delayed, Cancelled).
        delay_reason (str | None): Причина задержки рейса (если есть).
    """

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
        """
        Переводит рейс в статус 'Delayed' с указанием причины.

        Raises:
            ValueError: Если рейс уже отменен, находится в воздухе или приземлился.
        """
        if self.status in ["InFlight", "Landed", "Cancelled"]:
            raise ValueError(f"Невозможно отложить рейс в статусе {self.status}.")
        self.status = "Delayed"
        self.delay_reason = reason

    def cancel(self) -> None:
        """Полностью отменяет рейс."""
        self.status = "Cancelled"


class DepartureFlight(Flight):
    """
    Вылетающий рейс. Управляет процессом регистрации, багажом и посадкой.
    """

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
        """Безопасная копия списка зарегистрированных пассажиров."""
        return self._manifest.copy()

    @property
    def cargo_hold(self) -> list[Baggage]:
        """Безопасная копия списка загруженного багажа."""
        return self._cargo_hold.copy()

    def assign_gate(self, gate: Gate) -> None:
        """Привязывает инфраструктурный гейт к текущему рейсу."""
        self.assigned_gate = gate
        gate.assign_flight(self)

    def check_in_passenger(self, passenger: Passenger, ticket: Ticket) -> BoardingPass:
        """
        Регистрирует пассажира на рейс, гасит билет и генерирует посадочный талон.

        Raises:
            FlightDelayedException: Если регистрация закрыта или рейс отложен/отменен.
            InvalidTicketException: Если билет не принадлежит этому рейсу.
        """
        if self.status in ["Delayed", "Cancelled"]:
            raise FlightDelayedException(f"Регистрация невозможна: рейс {self.status}.")
        if ticket.flight_number != self.flight_number:
            raise InvalidTicketException("Билет оформлен на другой рейс.")

        ticket.use_ticket()
        self._manifest.append(passenger)

        # Алгоритм выдачи места (ряд + буква)
        row = (self._seat_counter // 6) + 1
        letter = chr(65 + (self._seat_counter % 6))
        seat_number = f"{row}{letter}"
        self._seat_counter += 1

        gate_number = self.assigned_gate.number if self.assigned_gate else "TBD"
        return BoardingPass(ticket, seat_number, gate_number)

    def load_baggage(self, baggage: Baggage) -> None:
        """Грузит проверенный багаж в трюм самолета."""
        baggage.check_weight()
        self._cargo_hold.append(baggage)

    def start_boarding(self) -> None:
        """Объявляет посадку и открывает привязанный гейт."""
        if not self.assigned_gate:
            raise ValueError("Гейт не назначен.")
        self.status = "Boarding"
        self.assigned_gate.open_gate()


class ArrivalFlight(Flight):
    """
    Прибывающий рейс. Взаимодействует с каруселями для выдачи багажа.
    """

    def __init__(
            self, flight_number: str, airline: Airline, aircraft: Aircraft, plan: FlightPlan
    ) -> None:
        super().__init__(flight_number, airline, aircraft, plan)
        self.assigned_carousel: BaggageCarousel | None = None
        self.status = "InFlight"

    def assign_carousel(self, carousel: BaggageCarousel) -> None:
        """Назначает карусель для выгрузки багажа пассажирам."""
        self.assigned_carousel = carousel

    def land(self) -> None:
        """Регистрирует приземление, меняет статус борта и запускает ленту багажа."""
        self.status = "Landed"
        self.aircraft.land()
        if self.assigned_carousel:
            self.assigned_carousel.activate(self)


class Schedule:
    """
    Электронное табло расписания рейсов (реестр полетов).
    """

    def __init__(self) -> None:
        self._flights: list[Flight] = []

    def add_flight(self, flight: Flight) -> None:
        """Добавляет рейс в общее расписание."""
        self._flights.append(flight)

    def get_departures(self) -> list[DepartureFlight]:
        """Возвращает список всех вылетающих рейсов."""
        return [f for f in self._flights if isinstance(f, DepartureFlight)]

    def get_arrivals(self) -> list[ArrivalFlight]:
        """Возвращает список всех прибывающих рейсов."""
        return [f for f in self._flights if isinstance(f, ArrivalFlight)]