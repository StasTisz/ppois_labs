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
        self._passengers: list[Passenger] = []
        self._employees: list[Employee] = []
        self._aircrafts: list[Aircraft] = []
        self._fuel_trucks: list[FuelTruck] = []
        self._tickets: list[Ticket] = []
        self._init_security_and_weather()

    def _init_security_and_weather(self) -> None:
        self.checkpoint = SecurityCheckpoint(number=1)
        self.checkpoint.assign_equipment(
            MetalDetector("Ceia PMD2"),
            XRayScanner("Smiths Heimann"),
        )
        self.current_weather = WeatherReport(
            temperature_c=18.0,
            wind_speed_ms=6.0,
            visibility_m=5000.0,
            is_stormy=False,
        )

    @property
    def passengers(self) -> list[Passenger]:
        return list(self._passengers)

    @property
    def employees(self) -> list[Employee]:
        return list(self._employees)

    @property
    def aircrafts(self) -> list[Aircraft]:
        return list(self._aircrafts)

    @property
    def fuel_trucks(self) -> list[FuelTruck]:
        return list(self._fuel_trucks)

    @property
    def tickets(self) -> list[Ticket]:
        return list(self._tickets)

    def register_aircraft(self, aircraft: Aircraft) -> None:
        if aircraft not in self._aircrafts:
            self._aircrafts.append(aircraft)

    def register_fuel_truck(self, truck: FuelTruck) -> None:
        if truck not in self._fuel_trucks:
            self._fuel_trucks.append(truck)

    def register_passenger(
        self,
        first_name: str | Passenger,
        last_name: str | None = None,
        passport_number: str | None = None,
    ) -> Passenger:
        if isinstance(first_name, Passenger):
            passenger = first_name
        else:
            passenger = Passenger(first_name, last_name or "", passport_number or "")
        if passenger not in self._passengers:
            self._passengers.append(passenger)
        return passenger

    def register_employee(self, employee: Employee) -> None:
        if employee not in self._employees:
            self._employees.append(employee)

    def find_passenger(self, passport_number: str) -> Passenger | None:
        for p in self._passengers:
            if p.passport_number == passport_number:
                return p
        return None

    def find_aircraft(self, tail_number: str) -> Aircraft | None:
        for a in self._aircrafts:
            if a.tail_number == tail_number:
                return a
        return None

    def find_departure_flight(self, flight_number: str) -> DepartureFlight | None:
        for f in self.schedule.get_departures():
            if f.flight_number == flight_number:
                return f
        return None

    def _resolve_passenger(self, passenger: Passenger | str) -> Passenger:
        passenger_obj = (
            passenger
            if isinstance(passenger, Passenger)
            else self.find_passenger(str(passenger))
        )
        if not passenger_obj:
            raise PassengerNotFoundException(
                f"Пассажир с паспортом {passenger} не найден."
            )
        return passenger_obj

    def _resolve_flight(self, flight: DepartureFlight | str) -> DepartureFlight:
        flight_obj = (
            flight
            if isinstance(flight, DepartureFlight)
            else self.find_departure_flight(str(flight))
        )
        if flight_obj is None:
            raise ValueError(f"Рейс {flight} не найден.")
        return flight_obj

    def issue_ticket(
        self,
        passenger: Passenger | str,
        flight: DepartureFlight | str,
        seat_class: str,
        price: float,
    ) -> Ticket:
        passenger_obj = self._resolve_passenger(passenger)
        flight_obj = self._resolve_flight(flight)
        ticket = Ticket(passenger_obj, flight_obj, seat_class, price)
        passenger_obj.buy_ticket(ticket)
        self._tickets.append(ticket)
        return ticket

    def create_departure_flight(
        self,
        flight_number: str,
        airline_name: str,
        tail_number: str,
        origin: str,
        destination: str,
        scheduled_time: datetime,
    ) -> DepartureFlight:
        aircraft = self.find_aircraft(tail_number)
        if not aircraft:
            raise ValueError(f"Самолет {tail_number} не найден во флоте.")

        airline = Airline(airline_name, flight_number[:2])
        plan = FlightPlan(origin, destination, scheduled_time)
        flight = DepartureFlight(flight_number, airline, aircraft, plan)

        self.schedule.add_flight(flight)
        return flight

    def _find_active_ticket(self, passenger: Passenger, flight_number: str) -> Ticket:
        ticket = next(
            (
                t
                for t in passenger.get_tickets()
                if t.flight_number == flight_number and not t.is_used
            ),
            None,
        )
        if not ticket:
            raise InvalidTicketException(
                f"У пассажира нет активного билета на рейс {flight_number}."
            )
        return ticket

    def check_in_passenger(
        self,
        passenger: Passenger | str,
        flight_number: str,
        baggage_weight: float | None = None,
    ) -> BoardingPass:
        passenger_obj = self._resolve_passenger(passenger)
        ticket = self._find_active_ticket(passenger_obj, flight_number)
        flight = self.find_departure_flight(flight_number)
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден в расписании вылетов.")

        if baggage_weight and baggage_weight > 0:
            baggage_obj = Baggage(baggage_weight, passenger_obj)
            passenger_obj.add_baggage(baggage_obj)
            flight.load_baggage(baggage_obj)

        return flight.check_in_passenger(passenger_obj, ticket)

    def prepare_flight(self, flight_number: str, fuel_amount: float = 3000.0) -> None:
        flight = self.find_departure_flight(flight_number)
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        inspection = MaintenanceInspection(flight.aircraft)
        tech = next((e for e in self._employees if e.is_on_shift), None)
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
        flight = self.find_departure_flight(flight_number)
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        if flight.aircraft.requires_maintenance:
            raise MaintenanceRequiredException(
                "Самолет не может взлететь: требуется предполетное ТО."
            )

        self.airport.control_tower.update_weather(
            self.current_weather.is_safe_for_operations
        )
        runway = self.airport.control_tower.request_takeoff(flight.aircraft)
        flight.aircraft.take_off()
        flight.status = "InFlight"
        runway.clear()
        return runway

    def __repr__(self) -> str:
        return (
            f"AirportFacade(airport={self.airport.name!r}, code={self.airport.iata_code!r}, "
            f"flights={len(self.schedule.get_departures())})"
        )
