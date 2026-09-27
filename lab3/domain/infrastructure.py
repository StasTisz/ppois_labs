import uuid
from typing import Any

from lab3.domain.exceptions import (
    CapacityExceededException,
    GateNotAssignedException,
    RunwayBusyException,
    WeatherWarningException,
)


class Runway:
    """
    Взлетно-посадочная полоса.

    Attributes:
        runway_id (str): Уникальный UUID полосы.
        number (str): Обозначение полосы (например, "27R").
        length (int): Длина полосы в метрах.
        is_busy (bool): Статус занятости.
        current_aircraft (Any | None): Борт, занимающий полосу в данный момент.
    """

    def __init__(self, number: str, length: int) -> None:
        self.runway_id = str(uuid.uuid4())
        self.number = number
        self.length = length
        self.is_busy = False
        self.current_aircraft: Any | None = None

    def occupy(self, aircraft: Any) -> None:
        """Занимает полосу конкретным бортом."""
        if self.is_busy:
            raise RunwayBusyException(f"Полоса {self.number} уже занята.")
        self.is_busy = True
        self.current_aircraft = aircraft

    def clear(self) -> None:
        """Освобождает полосу после завершения маневра."""
        self.is_busy = False
        self.current_aircraft = None


class Gate:
    """
    Выход на посадку.

    Attributes:
        gate_id (str): Уникальный UUID гейта.
        number (str): Номер гейта (например, "A12").
        is_open (bool): Статус посадки.
        current_flight (Any | None): Рейс, обслуживаемый в данный момент.
    """

    def __init__(self, number: str) -> None:
        self.gate_id = str(uuid.uuid4())
        self.number = number
        self.is_open = False
        self.current_flight: Any | None = None

    def assign_flight(self, flight: Any) -> None:
        """Привязывает рейс к гейту."""
        if self.current_flight is not None:
            raise ValueError(f"Гейт {self.number} уже обслуживает другой рейс.")
        self.current_flight = flight

    def open_gate(self) -> None:
        """Открывает гейт для начала посадки пассажиров."""
        if self.current_flight is None:
            raise GateNotAssignedException(f"Нельзя открыть гейт {self.number}: рейс не назначен.")
        self.is_open = True

    def close_gate(self) -> None:
        """Закрывает гейт (окончание посадки)."""
        self.is_open = False

    def clear_gate(self) -> None:
        """Освобождает гейт после отбытия рейса."""
        self.close_gate()
        self.current_flight = None


class CheckInCounter:
    """
    Стойка регистрации и приема багажа.

    Attributes:
        counter_id (str): UUID стойки.
        number (int): Номер стойки.
        is_open (bool): Работает ли стойка.
        current_agent (Any | None): Агент, работающий за стойкой (CheckInAgent).
        assigned_flight (Any | None): Рейс, на который идет регистрация.
    """

    def __init__(self, number: int) -> None:
        self.counter_id = str(uuid.uuid4())
        self.number = number
        self.is_open = False
        self.current_agent: Any | None = None
        self.assigned_flight: Any | None = None
        self._accepted_baggage: list[Any] = []

    def open_counter(self, agent: Any, flight: Any) -> None:
        """Открывает стойку регистрации для конкретного рейса."""
        self.current_agent = agent
        self.assigned_flight = flight
        self.is_open = True

    def close_counter(self) -> None:
        """Закрывает стойку и передает багаж в систему сортировки."""
        self.is_open = False
        self.current_agent = None
        self.assigned_flight = None
        self._accepted_baggage.clear()

    def accept_baggage(self, baggage: Any) -> None:
        """Принимает багаж пассажира."""
        if not self.is_open:
            raise ValueError("Стойка регистрации закрыта.")
        self._accepted_baggage.append(baggage)


class BaggageCarousel:
    """
    Багажная карусель для выдачи по прилету.
    """

    def __init__(self, number: int) -> None:
        self.carousel_id = str(uuid.uuid4())
        self.number = number
        self.is_active = False
        self.assigned_flight: Any | None = None

    def activate(self, flight: Any) -> None:
        """Запускает ленту для выдачи багажа прибывшего рейса."""
        self.assigned_flight = flight
        self.is_active = True

    def deactivate(self) -> None:
        """Останавливает ленту."""
        self.is_active = False
        self.assigned_flight = None


class Lounge:
    """
    Зал ожидания (включая бизнес-залы с ограничением вместимости).
    """

    def __init__(self, name: str, capacity: int, is_vip: bool = False) -> None:
        self.lounge_id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self.is_vip = is_vip
        self._passengers: list[Any] = []

    def enter(self, passenger: Any) -> None:
        """Регистрирует вход пассажира в зал ожидания."""
        if len(self._passengers) >= self.capacity:
            raise CapacityExceededException(f"Зал {self.name} переполнен.")
        # Здесь в будущем можно добавить проверку статуса билета для VIP-залов
        self._passengers.append(passenger)

    def exit(self, passenger: Any) -> None:
        """Регистрирует выход пассажира из зала."""
        if passenger in self._passengers:
            self._passengers.remove(passenger)

    @property
    def current_occupancy(self) -> int:
        return len(self._passengers)


class Terminal:
    """
    Пассажирский терминал, агрегирующий элементы инфраструктуры.
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
        """Поиск гейта по номеру."""
        for gate in self._gates:
            if gate.number == number:
                return gate
        return None


class ControlTower:
    """
    Диспетчерская вышка для управления воздушным движением.
    """

    def __init__(self) -> None:
        self.tower_id = str(uuid.uuid4())
        self._runways: list[Runway] = []
        self.weather_is_safe = True

    def add_runway(self, runway: Runway) -> None:
        self._runways.append(runway)

    def update_weather(self, is_safe: bool) -> None:
        """Обновление метеоусловий."""
        self.weather_is_safe = is_safe

    def request_takeoff(self, aircraft: Any) -> Runway:
        """
        Запрашивает разрешение на взлет и выделяет свободную ВПП.
        """
        if not self.weather_is_safe:
            raise WeatherWarningException("Взлет запрещен из-за сложных метеоусловий.")

        for runway in self._runways:
            if not runway.is_busy:
                runway.occupy(aircraft)
                return runway

        raise RunwayBusyException("Все ВПП заняты, ожидайте.")

    def request_landing(self, aircraft: Any) -> Runway:
        """
        Запрашивает разрешение на посадку.
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
    Ангар для ремонта и стоянки судов.
    """

    def __init__(self, number: str, capacity: int) -> None:
        self.hangar_id = str(uuid.uuid4())
        self.number = number
        self.capacity = capacity
        self._aircrafts: list[Any] = []

    def store_aircraft(self, aircraft: Any) -> None:
        """Помещает борт в ангар."""
        if len(self._aircrafts) >= self.capacity:
            raise CapacityExceededException(f"Ангар {self.number} заполнен.")
        self._aircrafts.append(aircraft)

    def release_aircraft(self, aircraft: Any) -> None:
        """Выпускает борт из ангара на перрон."""
        if aircraft in self._aircrafts:
            self._aircrafts.remove(aircraft)


class ParkingLot:
    """
    Парковка для автомобилей пассажиров и сотрудников.
    """

    def __init__(self, name: str, capacity: int) -> None:
        self.lot_id = str(uuid.uuid4())
        self.name = name
        self.capacity = capacity
        self._parked_cars: set[str] = set()

    def park_car(self, license_plate: str) -> None:
        """Регистрирует въезд автомобиля."""
        if len(self._parked_cars) >= self.capacity:
            raise CapacityExceededException(f"Парковка '{self.name}' переполнена.")
        self._parked_cars.add(license_plate)

    def remove_car(self, license_plate: str) -> None:
        """Регистрирует выезд автомобиля."""
        self._parked_cars.discard(license_plate)


class Airport:
    """
    Корневой агрегатор (фасад) инфраструктуры аэропорта.
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
        for t in self._terminals:
            if t.name == name:
                return t
        return None