"""
Модуль главного фасада аэропорта.

Реализует паттерн проектирования Facade, предоставляя единую высокоуровневую 
точку входа для управления всеми доменными подсистемами (инфраструктурой, 
флотом, операциями, безопасностью и персоналом). Инкапсулирует сложные сквозные 
бизнес-процессы, такие как подготовка рейса к вылету и регистрация пассажиров.
"""

from __future__ import annotations

from datetime import datetime

from lab3.domain.exceptions import (
    InvalidTicketException,
    MaintenanceRequiredException,
    PassengerNotFoundException,
)
from lab3.domain.fleet import Aircraft, FuelTruck
from lab3.domain.infrastructure import Airport, Runway
from lab3.domain.maintenance import MaintenanceInspection, RefuelingTask, WeatherReport
from lab3.domain.operations import (
    Airline,
    Baggage,
    BoardingPass,
    DepartureFlight,
    FlightPlan,
    Schedule,
    Ticket,
)
from lab3.domain.people import Employee, Passenger
from lab3.domain.security import MetalDetector, SecurityCheckpoint, XRayScanner


class AirportFacade:
    """
    Главный контроллер аэропорта.
    Оркестрирует реестры пассажиров, техники, расписание и погодные условия.
    """

    def __init__(self, airport_name: str, iata_code: str) -> None:
        self.airport = Airport(airport_name, iata_code)
        self.schedule = Schedule()

        # Защищенные реестры сущностей
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

    @property
    def passengers(self) -> dict[str, Passenger]:
        """Безопасная копия реестра зарегистрированных пассажиров."""
        return self._passengers.copy()

    @property
    def employees(self) -> dict[str, Employee]:
        """Безопасная копия реестра сотрудников аэропорта."""
        return self._employees.copy()

    @property
    def aircrafts(self) -> dict[str, Aircraft]:
        """Безопасная копия реестра флота воздушных судов."""
        return self._aircrafts.copy()

    @property
    def fuel_trucks(self) -> list[FuelTruck]:
        """Безопасная копия списка доступных топливозаправщиков."""
        return self._fuel_trucks.copy()

    @property
    def tickets(self) -> list[Ticket]:
        """Безопасная копия реестра выпущенных билетов."""
        return self._tickets.copy()

    # --- Управление инфраструктурой и флотом ---

    def register_aircraft(self, aircraft: Aircraft) -> None:
        """Добавляет воздушное судно в реестр аэропорта."""
        self._aircrafts[aircraft.tail_number] = aircraft

    def register_fuel_truck(self, truck: FuelTruck) -> None:
        """Добавляет топливозаправщик в перронную службу."""
        self._fuel_trucks.append(truck)

    def register_passenger(self, first_name: str, last_name: str, passport_number: str) -> Passenger:
        """Создает и регистрирует нового пассажира в системе."""
        passenger = Passenger(first_name, last_name, passport_number)
        self._passengers[passenger.passport_number] = passenger
        return passenger

    def register_employee(self, employee: Employee) -> None:
        """Принимает сотрудника на работу (добавляет в реестр)."""
        self._employees[employee.employee_id] = employee

    # --- Билеты и расписание ---

    def issue_ticket(self, passport_number: str, flight_number: str, seat_class: str, price: float) -> Ticket:
        """
        Оформляет и продает билет на рейс существующему пассажиру.

        Raises:
            PassengerNotFoundException: Если пассажир с таким паспортом не найден.
        """
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
        """
        Формирует вылетающий рейс и добавляет его в расписание.

        Raises:
            ValueError: Если указанный борт отсутствует в реестре флота.
        """
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
        Сквозной бизнес-процесс: поиск билета -> регистрация багажа -> выдача талона.

        Raises:
            PassengerNotFoundException: Если пассажир не зарегистрирован.
            InvalidTicketException: Если у пассажира нет активного билета на рейс.
            ValueError: Если рейс отсутствует в расписании вылетов.
        """
        passenger = self._passengers.get(passport_number)
        if not passenger:
            raise PassengerNotFoundException(f"Пассажир с паспортом {passport_number} не найден.")

        # Поиск первого неиспользованного билета на нужный рейс
        ticket = next(
            (t for t in passenger.get_tickets() if t.flight_number == flight_number and not t.is_used),
            None
        )
        if not ticket:
            raise InvalidTicketException(f"У пассажира нет активного билета на рейс {flight_number}.")

        # Поиск рейса в табло вылетов
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден в расписании вылетов.")

        # Обработка багажа, если он есть
        if baggage_weight and baggage_weight > 0:
            baggage_obj = Baggage(baggage_weight, passenger.person_id)
            passenger.add_baggage(baggage_obj)
            flight.load_baggage(baggage_obj)

        # Выполнение регистрации и выдача посадочного талона
        return flight.check_in_passenger(passenger, ticket)

    def prepare_flight(self, flight_number: str, fuel_amount: float = 3000.0) -> None:
        """
        Наземное обслуживание борта перед вылетом (ТО и дозаправка).

        Raises:
            ValueError: Если рейс не найден в расписании.
        """
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        # 1. Проведение регламентного ТО
        inspection = MaintenanceInspection(flight.aircraft)
        # Берем первого попавшегося сотрудника на смене для выполнения работы
        tech = next((e for e in self._employees.values() if e.is_on_shift), None)
        if tech:
            inspection.assign_staff(tech)
            inspection.execute()

        # 2. Перекачка топлива заправщиком
        if self._fuel_trucks and fuel_amount > 0:
            truck = self._fuel_trucks[0]
            refuel = RefuelingTask(flight.aircraft, truck, fuel_amount)
            if tech:
                refuel.assign_staff(tech)
                refuel.execute()

    def dispatch_takeoff(self, flight_number: str) -> Runway:
        """
        Запрашивает коридор у вышки и отправляет борт в рейс.

        Raises:
            ValueError: Если рейс не найден.
            MaintenanceRequiredException: Если борт не прошел ТО.
        """
        flight = next(
            (f for f in self.schedule.get_departures() if f.flight_number == flight_number),
            None
        )
        if not flight:
            raise ValueError(f"Рейс {flight_number} не найден.")

        if flight.aircraft.requires_maintenance:
            raise MaintenanceRequiredException("Самолет не может взлететь: требуется предполетное ТО.")

        # Обновляем сводку погоды на диспетчерской вышке перед запросом
        self.airport.control_tower.update_weather(self.current_weather.is_safe_for_operations)

        # Выделяем ВПП и совершаем взлет
        runway = self.airport.control_tower.request_takeoff(flight.aircraft)
        flight.aircraft.take_off()
        flight.status = "InFlight"

        # Освобождаем ВПП после отрыва борта
        runway.clear()
        return runway