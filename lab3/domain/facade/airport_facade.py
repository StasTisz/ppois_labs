from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import (
    InvalidTicketException,
    MaintenanceRequiredException,
    PassengerNotFoundException,
)
from lab3.domain.fleet.aircraft import Aircraft
from lab3.domain.fleet.fuel_truck import FuelTruck
from lab3.domain.infrastructure.airport import Airport
from lab3.domain.infrastructure.runway import Runway
from lab3.domain.maintenance.maintenance_inspection import MaintenanceInspection
from lab3.domain.maintenance.refueling_task import RefuelingTask
from lab3.domain.maintenance.weather_report import WeatherReport
from lab3.domain.operations.airline import Airline
from lab3.domain.operations.baggage import Baggage
from lab3.domain.operations.boarding_pass import BoardingPass
from lab3.domain.operations.departure_flight import DepartureFlight
from lab3.domain.operations.flight_plan import FlightPlan
from lab3.domain.operations.schedule import Schedule
from lab3.domain.operations.ticket import Ticket
from lab3.domain.people.employee import Employee
from lab3.domain.people.passenger import Passenger
from lab3.domain.security.metal_detector import MetalDetector
from lab3.domain.security.security_checkpoint import SecurityCheckpoint
from lab3.domain.security.xray_scanner import XRayScanner

if TYPE_CHECKING:
    from datetime import datetime


class AirportFacade:
    def __init__(self, airport_name: str, iata_code: str) -> None:
        self.airport = Airport(airport_name, iata_code)
        self.schedule = Schedule()

        self._passengers: dict[str, Passenger] = {}
        self._employees: dict[str, Employee] = {}
        self._aircrafts: dict[str, Aircraft] = {}
        self._fuel_trucks: list[FuelTruck] = []
        self._tickets: list[Ticket] = []

        self.checkpoint = SecurityCheckpoint(number=1)
        self.checkpoint.assign_equipment(
            MetalDetector("Ceia PMD2"),
            XRayScanner("Smiths Heimann")
        )

        self.current_weather = WeatherReport(
            temperature_c=18.0,
            wind_speed_ms=6.0,
            visibility_m=5000.0,
            is_stormy=False
        )

    @property
    def passengers(self) -> dict[str, Passenger]:
        return self._passengers.copy()

    @property
    def employees(self) -> dict[str, Employee]:
        return self._employees.copy()

    @property
    def aircrafts(self) -> dict[str, Aircraft]:
        return self._aircrafts.copy()

    @property
    def fuel_trucks(self) -> list[FuelTruck]:
        return self._fuel_trucks.copy()

    @property
    def tickets(self) -> list[Ticket]:
        return self._tickets.copy()

    def register_aircraft(self, aircraft: Aircraft) -> None:
        self._aircrafts[aircraft.tail_number] = aircraft

    def register_fuel_truck(self, truck: FuelTruck) -> None:
        self._fuel_trucks.append(truck)

    def register_passenger(self, first_name: str, last_name: str, passport_number: str) -> Passenger:
        passenger = Passenger(first_name, last_name, passport_number)
        self._passengers[passenger.passport_number] = passenger
        return passenger

    def register_employee(self, employee: Employee) -> None:
        self._employees[employee.employee_id] = employee

    def issue_ticket(self, passport_number: str, flight_number: str, seat_class: str, price: float) -> Ticket:
        passenger = self._passengers.get(passport_number)
        if not passenger:
            raise PassengerNotFoundException(f"Пассажир с паспортом {passport_number} не найден.")

        flight = next((f for f in self.schedule.get_departures() if f.flight_number == flight_number), flight_number)
        ticket = Ticket(passenger, flight, seat_class, price)
        passenger.buy_ticket(ticket)
        self._tickets.append(ticket)
        return ticket

    def create_departure_flight(
            self, flight_number: str, airline_name: str, tail_number: str,
            origin: str, destination: str, scheduled_time: datetime
    ) -> DepartureFlight:
        aircraft = self._aircrafts.get(tail_number)
        if not aircraft:
            raise ValueError(f"Самолет {tail_number} не найден во флоте.")

        airline = Airline(airline_name, flight_number[:2])
        plan = FlightPlan(origin, destination, scheduled_time)
        flight = DepartureFlight(flight_number, airline, aircraft, plan)

        self.schedule.add_flight(flight)
        return flight

    def check_in_passenger(
            self, passport_number: str, flight_number: str, baggage_weight: float | None = None
    ) -> BoardingPass:
        passenger = self._passengers.get(passport_number)
        if not passenger:
            raise PassengerNotFoundException(f"Пассажир с паспортом {passport_number} не найден.")

        ticket = next(
            (t for t in passenger.get_tickets() if t.flight_number == flight_number and not t.is_used),
            None
        )
        if not ticket:
            raise InvalidTicketException(f"У пассажира нет активного билета на рейс {flight_number}.")

        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден в расписании вылетов.")

        if baggage_weight and baggage_weight > 0:
            baggage_obj = Baggage(baggage_weight, passenger)
            passenger.add_baggage(baggage_obj)
            flight.load_baggage(baggage_obj)

        return flight.check_in_passenger(passenger, ticket)

    def prepare_flight(self, flight_number: str, fuel_amount: float = 3000.0) -> None:
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        inspection = MaintenanceInspection(flight.aircraft)
        tech = next((e for e in self._employees.values() if e.is_on_shift), None)
        if tech:
            inspection.assign_staff(tech)
            inspection.execute()

        if self._fuel_trucks and fuel_amount > 0:
            truck = self._fuel_trucks[0]
            refuel = RefuelingTask(flight.aircraft, truck, fuel_amount)
            if tech:
                refuel.assign_staff(tech)
                refuel.execute()

    def dispatch_takeoff(self, flight_number: str) -> Runway:
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        if flight.aircraft.requires_maintenance:
            raise MaintenanceRequiredException("Самолет не может взлететь: требуется предполетное ТО.")

        self.airport.control_tower.update_weather(self.current_weather.is_safe_for_operations)
        runway = self.airport.control_tower.request_takeoff(flight.aircraft)
        flight.aircraft.take_off()
        flight.status = "InFlight"
        runway.clear()
        return runway
