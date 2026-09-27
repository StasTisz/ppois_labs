import uuid
from datetime import datetime

from lab3.domain.exceptions import (
    GateNotAssignedException,
    InvalidTicketException,
    MaintenanceRequiredException,
    NoAvailableCrewException,
    PassengerNotFoundException,
    SecurityCheckFailedException,
    WeatherWarningException,
)
from lab3.domain.fleet import Aircraft, FuelTruck, PassengerAircraft
from lab3.domain.infrastructure import Airport, Gate, Runway, Terminal
from lab3.domain.maintenance import MaintenanceInspection, RefuelingTask, WeatherReport
from lab3.domain.operations import (
    Baggage,
    BoardingPass,
    DepartureFlight,
    Flight,
    FlightPlan,
    Schedule,
    Ticket,
)
from lab3.domain.people import Employee, Passenger, Pilot
from lab3.domain.security import MetalDetector, SecurityCheckpoint, XRayScanner


class AirportFacade:
    """
    Главный фасад аэропорта (Controller / Facade).
    Оркестрирует взаимодействие всех доменных подсистем.
    """

    def __init__(self, airport_name: str, iata_code: str) -> None:
        self.airport = Airport(airport_name, iata_code)
        self.schedule = Schedule()

        # Реестры сущностей
        self._passengers: dict[str, Passenger] = {}
        self._employees: dict[str, Employee] = {}
        self._aircrafts: dict[str, Aircraft] = {}
        self._fuel_trucks: list[FuelTruck] = []
        self._tickets: list[Ticket] = []

        # Пункт досмотра по умолчанию
        self.checkpoint = SecurityCheckpoint(number=1)
        self.checkpoint.assign_equipment(
            MetalDetector("Ceia PMD2"),
            XRayScanner("Smiths Heimann")
        )

        # Текущая погода (по умолчанию летная)
        self.current_weather = WeatherReport(
            temperature_c=18.0,
            wind_speed_ms=6.0,
            visibility_m=5000.0,
            is_stormy=False
        )

    # --- Управление инфраструктурой и флотом ---

    def register_aircraft(self, aircraft: Aircraft) -> None:
        """Добавляет воздушное судно в реестр."""
        self._aircrafts[aircraft.tail_number] = aircraft

    def register_fuel_truck(self, truck: FuelTruck) -> None:
        """Добавляет топливозаправщик в перронную службу."""
        self._fuel_trucks.append(truck)

    def register_passenger(self, first_name: str, last_name: str, passport_number: str) -> Passenger:
        """Регистрирует нового пассажира в системе."""
        passenger = Passenger(first_name, last_name, passport_number)
        self._passengers[passenger.passport_number] = passenger
        return passenger

    def register_employee(self, employee: Employee) -> None:
        """Принимает сотрудника на работу."""
        self._employees[employee.employee_id] = employee

    # --- Билеты и расписание ---

    def issue_ticket(self, passport_number: str, flight_number: str, seat_class: str, price: float) -> Ticket:
        """Оформляет билет на рейс."""
        passenger = self._passengers.get(passport_number)
        if not passenger:
            raise PassengerNotFoundException(f"Пассажир с паспортом {passport_number} не найден.")

        ticket = Ticket(passenger.person_id, flight_number, seat_class, price)
        passenger.buy_ticket(ticket)
        self._tickets.append(ticket)
        return ticket

    def create_departure_flight(
            self, flight_number: str, airline_name: str, tail_number: str,
            origin: str, destination: str, scheduled_time: datetime
    ) -> DepartureFlight:
        """Создает и регистрирует вылетающий рейс в расписании."""
        from lab3.domain.operations import Airline

        aircraft = self._aircrafts.get(tail_number)
        if not aircraft:
            raise ValueError(f"Самолет {tail_number} не найден во флоте.")

        airline = Airline(airline_name, flight_number[:2])
        plan = FlightPlan(origin, destination, scheduled_time)
        flight = DepartureFlight(flight_number, airline, aircraft, plan)

        self.schedule.add_flight(flight)
        return flight

    # --- Сквозные сценарии обслуживания ---

    def check_in_passenger(
            self, passport_number: str, flight_number: str, baggage_weight: float | None = None
    ) -> BoardingPass:
        """
        Сквозной процесс: проверка билета -> досмотр СБ -> сдача багажа -> выдача талона.
        """
        passenger = self._passengers.get(passport_number)
        if not passenger:
            raise PassengerNotFoundException(f"Пассажир с паспортом {passport_number} не найден.")

        # Поиск неиспользованного билета на этот рейс
        ticket = next(
            (t for t in passenger.get_tickets() if t.flight_number == flight_number and not t.is_used),
            None
        )
        if not ticket:
            raise InvalidTicketException(f"У пассажира нет активного билета на рейс {flight_number}.")

        # Поиск рейса
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден в расписании вылетов.")

        # Обработка багажа, если есть
        baggage_obj = None
        if baggage_weight and baggage_weight > 0:
            baggage_obj = Baggage(baggage_weight, passenger.person_id)
            passenger.add_baggage(baggage_obj)
            flight.load_baggage(baggage_obj)

        # Регистрация пассажира на рейс
        return flight.check_in_passenger(passenger, ticket)

    def prepare_flight(self, flight_number: str, fuel_amount: float = 3000.0) -> None:
        """
        Наземное обслуживание борта: ТО и заправка перед вылетом.
        """
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        # 1. Проведение ТО
        inspection = MaintenanceInspection(flight.aircraft)
        # Назначаем первого попавшегося сотрудника
        tech = next((e for e in self._employees.values() if e.is_on_shift), None)
        if tech:
            inspection.assign_staff(tech)
            inspection.execute()

        # 2. Заправка
        if self._fuel_trucks and fuel_amount > 0:
            truck = self._fuel_trucks[0]
            refuel = RefuelingTask(flight.aircraft, truck, fuel_amount)
            if tech:
                refuel.assign_staff(tech)
                refuel.execute()

    def dispatch_takeoff(self, flight_number: str) -> Runway:
        """
        Выполнение взлета: проверка готовности, метеоусловий и выделение полосы.
        """
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        if flight.aircraft.requires_maintenance:
            raise MaintenanceRequiredException("Самолет не может взлететь: требуется предполетное ТО.")

        # Обновляем погоду на вышке перед запросом
        self.airport.control_tower.update_weather(self.current_weather.is_safe_for_operations)

        # Выделяем полосу
        runway = self.airport.control_tower.request_takeoff(flight.aircraft)
        flight.aircraft.take_off()
        flight.status = "InFlight"

        # Полоса освобождается после разбега
        runway.clear()
        return runway