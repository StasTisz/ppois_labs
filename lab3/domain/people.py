import uuid
from abc import ABC, abstractmethod
from typing import Any


class Person:
    """
    Базовый класс для всех физических лиц в системе аэропорта.

    Attributes:
        person_id (str): Уникальный внутренний идентификатор.
        first_name (str): Имя.
        last_name (str): Фамилия.
        passport_number (str): Номер документа, удостоверяющего личность.
    """

    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        self.person_id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.passport_number = passport_number

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Passenger(Person):
    """
    Клиент аэропорта (пассажир).

    Attributes:
        is_boarded (bool): Статус посадки на рейс.
    """

    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        super().__init__(first_name, last_name, passport_number)
        self.is_boarded = False
        self._tickets: list[Any] = []  # В будущем список объектов Ticket
        self._baggage: list[Any] = []  # В будущем список объектов Baggage

    def buy_ticket(self, ticket: Any) -> None:
        """Покупка и привязка билета к пассажиру."""
        self._tickets.append(ticket)

    def add_baggage(self, baggage_item: Any) -> None:
        """Добавление единицы багажа пассажиру."""
        self._baggage.append(baggage_item)

    @property
    def has_tickets(self) -> bool:
        return len(self._tickets) > 0

    @property
    def baggage_count(self) -> int:
        return len(self._baggage)

    def get_tickets(self) -> list[Any]:
        return self._tickets.copy()


class Employee(Person, ABC):
    """
    Базовый абстрактный класс для всех сотрудников аэропорта и авиакомпаний.

    Attributes:
        employee_id (str): Табельный номер сотрудника.
        salary (float): Базовая ставка или оклад.
        is_on_shift (bool): Находится ли сотрудник на смене.
    """

    def __init__(self, first_name: str, last_name: str, passport_number: str, salary: float) -> None:
        super().__init__(first_name, last_name, passport_number)
        self.employee_id = str(uuid.uuid4())
        self.salary = salary
        self.is_on_shift = False

    def clock_in(self) -> None:
        """Начать рабочую смену."""
        self.is_on_shift = True

    def clock_out(self) -> None:
        """Завершить рабочую смену."""
        self.is_on_shift = False

    @abstractmethod
    def perform_duty(self) -> str:
        """
        Полиморфный метод выполнения рабочих обязанностей.
        Обязателен для переопределения во всех дочерних должностях.
        """
        pass


class CrewMember(Employee, ABC):
    """
    Абстрактный класс для летного состава (пилоты, бортпроводники).

    Attributes:
        flight_hours (int): Количество часов налета.
        max_monthly_hours (int): Санитарная норма часов налета в месяц.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, max_monthly_hours: int = 90
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.flight_hours = 0
        self.max_monthly_hours = max_monthly_hours

    def log_flight_hours(self, hours: int) -> None:
        """Фиксирует часы, проведенные в рейсе."""
        if self.flight_hours + hours > self.max_monthly_hours:
            raise ValueError(f"Превышена санитарная норма налета ({self.max_monthly_hours} ч.)")
        self.flight_hours += hours


class Pilot(CrewMember):
    """
    Пилот воздушного судна.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, license_type: str, is_captain: bool = False
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.license_type = license_type
        self.is_captain = is_captain
        self.pre_flight_checks_done = False

    def perform_duty(self) -> str:
        """Обязанность пилота: предрейсовый осмотр и пилотирование."""
        if not self.is_on_shift:
            raise ValueError(f"Пилот {self.full_name} не на смене.")

        self.pre_flight_checks_done = True
        role = "КВС (Капитан)" if self.is_captain else "Второй пилот"
        return f"{role} {self.full_name} выполнил чек-лист и готов к вылету."


class FlightAttendant(CrewMember):
    """
    Бортпроводник (стюард / стюардесса).
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, languages: list[str]
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.languages = languages
        self.safety_briefing_done = False

    def perform_duty(self) -> str:
        """Обязанность бортпроводника: инструктаж и обслуживание пассажиров."""
        if not self.is_on_shift:
            raise ValueError(f"Бортпроводник {self.full_name} не на смене.")

        self.safety_briefing_done = True
        return f"Бортпроводник {self.full_name} провел инструктаж по безопасности."


class Dispatcher(Employee):
    """
    Авиадиспетчер. Управляет трафиком с диспетчерской вышки.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, clearance_level: int
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.clearance_level = clearance_level
        self.active_channels: int = 0

    def perform_duty(self) -> str:
        """Обязанность диспетчера: мониторинг радиочастот и выдача разрешений."""
        self.active_channels = 3
        return f"Диспетчер {self.full_name} ведет радиообмен на {self.active_channels} каналах."


class SecurityOfficer(Employee):
    """
    Сотрудник службы безопасности аэропорта (досмотр, рамки).
    """

    def perform_duty(self) -> str:
        """Обязанность СБ: мониторинг камер и интроскопов."""
        return f"Офицер СБ {self.full_name} осуществляет досмотр в зоне контроля."


class CheckInAgent(Employee):
    """
    Агент службы организации пассажирских перевозок (на стойке регистрации).
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, typing_speed: int
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.typing_speed = typing_speed
        self.passengers_processed = 0

    def perform_duty(self) -> str:
        """Обязанность агента: регистрация пассажиров и оформление багажа."""
        self.passengers_processed += 1
        return f"Агент {self.full_name} зарегистрировал пассажира (итого: {self.passengers_processed})."


class BaggageHandler(Employee):
    """
    Грузчик багажного отделения.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, heavy_machinery_license: bool
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.heavy_machinery_license = heavy_machinery_license
        self.tons_loaded = 0.0

    def perform_duty(self) -> str:
        """Обязанность грузчика: погрузка чемоданов в трюм самолета."""
        self.tons_loaded += 0.5
        equipment = "с помощью погрузчика" if self.heavy_machinery_license else "вручную"
        return f"Грузчик {self.full_name} переместил багаж {equipment}."