"""
Модуль инфраструктуры аэропорта.

Содержит классы, описывающие физические и логические объекты на территории аэропорта.
Служит основой для взаимодействия флота и пассажиров.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import (
    CapacityExceededException,
    GateNotAssignedException,
    RunwayBusyException,
    WeatherWarningException,
)

# позволяя линтеру (mypy) и IDE видеть реальные классы при проверке типов.
if TYPE_CHECKING:
    from lab3.domain.fleet import Aircraft
    from lab3.domain.operations import Baggage, Flight
    from lab3.domain.people import CheckInAgent, Passenger


class Runway:
    """
    Взлетно-посадочная полоса.
    Отвечает за координацию занятости при взлетах и посадках.

    Attributes:
        runway_id (str): Внутренний уникальный идентификатор.
        number (str): Навигационное обозначение полосы (например, "27R").
        length (int): Длина полосы в метрах (влияет на типы принимаемых судов).
        is_busy (bool): Флаг текущей занятости маневрирующим бортом.
        current_aircraft (Aircraft | None): Борт, находящийся на полосе.
    """

    def __init__(self, number: str, length: int) -> None:
        self.runway_id = str(uuid.uuid4())
        self.number = number
        self.length = length
        self.is_busy = False
        self.current_aircraft: Aircraft | None = None

    def occupy(self, aircraft: Aircraft) -> None:
        """
        Занимает полосу указанным воздушным судном.

        Raises:
            RunwayBusyException: Если полоса уже занята другим бортом.
        """
        if self.is_busy:
            raise RunwayBusyException(f"Полоса {self.number} уже занята.")
        self.is_busy = True
        self.current_aircraft = aircraft

    def clear(self) -> None:
        """Освобождает полосу после завершения взлета или руления на перрон."""
        self.is_busy = False
        self.current_aircraft = None


class Gate:
    """
    Выход на посадку (гейт) в терминале.
    Связывает инфраструктуру терминала с конкретным авиарейсом.

    Attributes:
        gate_id (str): Внутренний уникальный идентификатор.
        number (str): Номер гейта для табло (например, "A12").
        is_open (bool): Открыта ли физически посадка пассажиров.
        current_flight (Flight | None): Рейс, обслуживаемый у данного гейта.
    """

    def __init__(self, number: str) -> None:
        self.gate_id = str(uuid.uuid4())
        self.number = number
        self.is_open = False
        self.current_flight: Flight | None = None

    def assign_flight(self, flight: Flight) -> None:
        """
        Привязывает рейс к гейту для подготовки к посадке.

        Raises:
            ValueError: Если гейт не освобожден от предыдущего рейса.
        """
        if self.current_flight is not None:
            raise ValueError(f"Гейт {self.number} уже обслуживает другой рейс.")
        self.current_flight = flight

    def open_gate(self) -> None:
        """Открывает двери гейта для посадки по талонам."""
        if self.current_flight is None:
            raise GateNotAssignedException(f"Нельзя открыть гейт {self.number}: рейс не назначен.")
        self.is_open = True

    def close_gate(self) -> None:
        """Останавливает пропуск пассажиров на рейс."""
        self.is_open = False

    def clear_gate(self) -> None:
        """Полностью освобождает гейт после отбытия судна."""
        self.close_gate()
        self.current_flight = None


class CheckInCounter:
    """
    Стойка регистрации пассажиров и приема багажа.

    Attributes:
        counter_id (str): Внутренний уникальный идентификатор.
        number (int): Номер стойки регистрации.
        is_open (bool): Статус работы.
        current_agent (CheckInAgent | None): Сотрудник, авторизованный за стойкой.
        assigned_flight (Flight | None): Рейс, на который ведется прием.
    """

    def __init__(self, number: int) -> None:
        self.counter_id = str(uuid.uuid4())
        self.number = number
        self.is_open = False
        self.current_agent: CheckInAgent | None = None
        self.assigned_flight: Flight | None = None
        self._accepted_baggage: list[Baggage] = []

    def open_counter(self, agent: CheckInAgent, flight: Flight) -> None:
        """Открывает смену на стойке регистрации."""
        self.current_agent = agent
        self.assigned_flight = flight
        self.is_open = True

    def close_counter(self) -> None:
        """Закрывает стойку и отправляет принятый багаж в систему сортировки."""
        self.is_open = False
        self.current_agent = None
        self.assigned_flight = None
        self._accepted_baggage.clear()

    def accept_baggage(self, baggage: Baggage) -> None:
        """Принимает единицу багажа на конвейерную ленту."""
        if not self.is_open:
            raise ValueError("Стойка регистрации закрыта.")
        self._accepted_baggage.append(baggage)


class BaggageCarousel:
    """
    Багажная карусель для выдачи чемоданов по прилету.
    """

    def __init__(self, number: int) -> None:
        self.carousel_id = str(uuid.uuid4())
        self.number = number
        self.is_active = False
        self.assigned_flight: Flight | None = None

    def activate(self, flight: Flight) -> None:
        """Привязывает карусель к рейсу и запускает конвейер."""
        self.assigned_flight = flight
        self.is_active = True

    def deactivate(self) -> None:
        """Останавливает конвейер после выдачи всего багажа."""
        self.is_active = False
        self.assigned_flight = None


class Lounge:
    """
    Зал ожидания для пассажиров (бизнес-залы, VIP-комнаты).
    """

    def __init__(self, name: str, capacity: int, is_vip: bool = False) -> None:
        self.lounge_id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self.is_vip = is_vip
        self._passengers: list[Passenger] = []

    def enter(self, passenger: Passenger) -> None:
        """Впускает пассажира с проверкой лимита вместимости."""
        if len(self._passengers) >= self.capacity:
            raise CapacityExceededException(f"Зал {self.name} переполнен.")
        self._passengers.append(passenger)

    def exit(self, passenger: Passenger) -> None:
        """Регистрирует выход пассажира из зала."""
        if passenger in self._passengers:
            self._passengers.remove(passenger)

    @property
    def current_occupancy(self) -> int:
        return len(self._passengers)


class Terminal:
    """
    Пассажирский терминал. Агрегирует гейты, стойки, залы и карусели в единый хаб.
    """

    def __init__(self, name: str) -> None:
        self.terminal_id = str(uuid.uuid4())
        self.name = name
        self._gates: list[Gate] = []
        self._check_in_counters: list[CheckInCounter] = []
        self._carousels: list[BaggageCarousel] = []
        self._lounges: list[Lounge] = []

    def add_gate(self, gate: Gate) -> None:
        self._gates.append(gate)

    def add_counter(self, counter: CheckInCounter) -> None:
        self._check_in_counters.append(counter)

    def add_carousel(self, carousel: BaggageCarousel) -> None:
        self._carousels.append(carousel)

    def add_lounge(self, lounge: Lounge) -> None:
        self._lounges.append(lounge)

    def get_gate(self, number: str) -> Gate | None:
        """Возвращает объект гейта по его строковому номеру (например, 'A1')."""
        for gate in self._gates:
            if gate.number == number:
                return gate
        return None


class ControlTower:
    """
    Диспетчерская вышка. Центральный орган управления воздушным движением.
    Отвечает за выдачу разрешений на взлет/посадку с учетом метеоусловий.
    """

    def __init__(self) -> None:
        self.tower_id = str(uuid.uuid4())
        self._runways: list[Runway] = []
        self.weather_is_safe = True

    def add_runway(self, runway: Runway) -> None:
        """Берет ВПП под управление вышки."""
        self._runways.append(runway)

    def update_weather(self, is_safe: bool) -> None:
        """Обновляет статус безопасности метеоусловий."""
        self.weather_is_safe = is_safe

    def request_takeoff(self, aircraft: Aircraft) -> Runway:
        """
        Запрашивает коридор для взлета.

        Raises:
            WeatherWarningException: При штормовом предупреждении.
            RunwayBusyException: Если нет свободных полос.
        """
        if not self.weather_is_safe:
            raise WeatherWarningException("Взлет запрещен из-за сложных метеоусловий.")

        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway

        raise RunwayBusyException("Все ВПП заняты, ожидайте слота.")

    def request_landing(self, aircraft: Aircraft) -> Runway:
        """
        Запрашивает коридор для посадки.
        """
        if not self.weather_is_safe:
            raise WeatherWarningException("Посадка запрещена (аэропорт закрыт по метеоусловиям).")

        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway

        raise RunwayBusyException("Борт отправлен в зону ожидания: все ВПП заняты.")


class Hangar:
    """
    Технический ангар для длительной стоянки и ремонта воздушных судов.
    """

    def __init__(self, number: str, capacity: int) -> None:
        self.hangar_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self._aircrafts: list[Aircraft] = []

    def store_aircraft(self, aircraft: Aircraft) -> None:
        """Отправляет борт в ангар с проверкой наличия мест."""
        if len(self._aircrafts) >= self.capacity:
            raise CapacityExceededException(f"Ангар {self.number} заполнен.")
        self._aircrafts.append(aircraft)

    def release_aircraft(self, aircraft: Aircraft) -> None:
        """Выпускает борт из ангара на перрон."""
        if aircraft in self._aircrafts:
            self._aircrafts.remove(aircraft)


class ParkingLot:
    """
    Паркинг для автомобилей клиентов и сотрудников аэропорта.
    """

    def __init__(self, name: str, capacity: int) -> None:
        self.lot_id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self._parked_cars: set[str] = set()

    def park_car(self, license_plate: str) -> None:
        """Осуществляет въезд автомобиля на паркинг."""
        if len(self._parked_cars) >= self.capacity:
            raise CapacityExceededException(f"Парковка '{self.name}' переполнена.")
        self._parked_cars.add(license_plate)

    def remove_car(self, license_plate: str) -> None:
        """Освобождает парковочное место."""
        self._parked_cars.discard(license_plate)


class Airport:
    """
    Агрегатор верхнего уровня. Представляет физический аэропорт в целом.
    Объединяет терминалы, парковки, вышку и ангары.
    """

    def __init__(self, name: str, iata_code: str) -> None:
        self.name = name
        self.iata_code = iata_code
        self.control_tower = ControlTower()
        self._terminals: list[Terminal] = []
        self._hangars: list[Hangar] = []
        self._parking_lots: list[ParkingLot] = []

    def add_terminal(self, terminal: Terminal) -> None:
        self._terminals.append(terminal)

    def get_terminal(self, name: str) -> Terminal | None:
        """Ищет терминал по его названию (например, 'Terminal 1')."""
        for t in self._terminals:
            if t.name == name:
                return t
        return None