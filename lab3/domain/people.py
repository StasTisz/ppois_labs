"""
Модуль физических лиц аэропорта.

Содержит иерархию классов для всех людей, взаимодействующих с системой:
пассажиров (клиентов) и персонала (экипажи, диспетчеры, агенты, грузчики).
Реализует паттерн полиморфизма через метод perform_duty() для всех сотрудников
и инкапсулирует статистику работы (часы налета, количество обработанных грузов).
"""

from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Защита от циклических импортов.
# Эти классы нужны только для аннотаций типов в методах Passenger.
if TYPE_CHECKING:
    from lab3.domain.operations import Baggage, Ticket


class Person:
    """
    Базовый класс для всех физических лиц в системе.

    Attributes:
        person_id (str): Внутренний уникальный идентификатор.
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
        """Возвращает полное имя персоны (Имя + Фамилия)."""
        return f"{self.first_name} {self.last_name}"


class Passenger(Person):
    """
    Клиент аэропорта (пассажир). Управляет своими билетами и багажом.
    """

    def __init__(self, first_name: str, last_name: str, passport_number: str) -> None:
        super().__init__(first_name, last_name, passport_number)
        self.is_boarded = False
        self._tickets: list[Ticket] = []
        self._baggage: list[Baggage] = []

    def buy_ticket(self, ticket: Ticket) -> None:
        """Привязывает купленный билет к профилю пассажира."""
        self._tickets.append(ticket)

    def add_baggage(self, baggage_item: Baggage) -> None:
        """Регистрирует единицу багажа на пассажира."""
        self._baggage.append(baggage_item)

    @property
    def has_tickets(self) -> bool:
        """Проверяет наличие хотя бы одного билета."""
        return len(self._tickets) > 0

    @property
    def baggage_count(self) -> int:
        """Возвращает количество мест багажа."""
        return len(self._baggage)

    def get_tickets(self) -> list[Ticket]:
        """
        Возвращает копию списка билетов.
        Копия гарантирует, что внешний код не сможет изменить оригинальный список.
        """
        return self._tickets.copy()


class Employee(Person, ABC):
    """
    Базовый абстрактный класс для всех сотрудников.

    Attributes:
        employee_id (str): Табельный номер сотрудника.
        salary (float): Базовый оклад.
        is_on_shift (bool): Статус нахождения на рабочем месте.
    """

    def __init__(self, first_name: str, last_name: str, passport_number: str, salary: float) -> None:
        super().__init__(first_name, last_name, passport_number)
        self.employee_id = str(uuid.uuid4())
        self.salary = salary
        self.is_on_shift = False

    def clock_in(self) -> None:
        """Начинает рабочую смену сотрудника."""
        self.is_on_shift = True

    def clock_out(self) -> None:
        """Завершает рабочую смену."""
        self.is_on_shift = False

    @abstractmethod
    def perform_duty(self) -> str:
        """
        Полиморфный метод выполнения профессиональных обязанностей.
        Каждая должность реализует свою уникальную логику.
        """
        pass


class CrewMember(Employee, ABC):
    """
    Абстрактный класс летного состава (экипажа).
    Вводит контроль санитарной нормы часов налета.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, max_monthly_hours: int = 90
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.max_monthly_hours = max_monthly_hours
        self._flight_hours = 0

    @property
    def flight_hours(self) -> int:
        """Текущее количество часов налета за месяц."""
        return self._flight_hours

    def log_flight_hours(self, hours: int) -> None:
        """
        Фиксирует часы в рейсе.

        Raises:
            ValueError: При попытке превысить санитарную норму налета.
        """
        if self._flight_hours + hours > self.max_monthly_hours:
            raise ValueError(f"Превышена санитарная норма налета ({self.max_monthly_hours} ч.)")
        self._flight_hours += hours


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
        """Выполняет предрейсовый чек-лист и пилотирование."""
        if not self.is_on_shift:
            raise ValueError(f"Пилот {self.full_name} не на смене.")

        self.pre_flight_checks_done = True
        role = "КВС (Капитан)" if self.is_captain else "Второй пилот"
        return f"{role} {self.full_name} выполнил чек-лист и готов к вылету."


class FlightAttendant(CrewMember):
    """
    Бортпроводник.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, languages: list[str]
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.languages = languages
        self.safety_briefing_done = False

    def perform_duty(self) -> str:
        """Проводит инструктаж и обеспечивает безопасность салона."""
        if not self.is_on_shift:
            raise ValueError(f"Бортпроводник {self.full_name} не на смене.")

        self.safety_briefing_done = True
        return f"Бортпроводник {self.full_name} провел инструктаж по безопасности."


class Dispatcher(Employee):
    """
    Авиадиспетчер вышки управления движением.
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, clearance_level: int
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.clearance_level = clearance_level
        self.active_channels: int = 0

    def perform_duty(self) -> str:
        """Мониторит частоты и координирует взлеты/посадки."""
        self.active_channels = 3
        return f"Диспетчер {self.full_name} ведет радиообмен на {self.active_channels} каналах."


class SecurityOfficer(Employee):
    """
    Офицер службы авиационной безопасности (САБ).
    """

    def perform_duty(self) -> str:
        """Осуществляет досмотр пассажиров и багажа."""
        return f"Офицер СБ {self.full_name} осуществляет досмотр в зоне контроля."


class CheckInAgent(Employee):
    """
    Агент службы организации перевозок (работает за стойкой).
    """

    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, typing_speed: int
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.typing_speed = typing_speed
        self._passengers_processed = 0

    @property
    def passengers_processed(self) -> int:
        """Количество зарегистрированных агентом пассажиров за смену."""
        return self._passengers_processed

    def perform_duty(self) -> str:
        """Оформляет пассажира на рейс."""
        self._passengers_processed += 1
        return f"Агент {self.full_name} зарегистрировал пассажира (итого: {self._passengers_processed})."


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
        self._tons_loaded = 0.0

    @property
    def tons_loaded(self) -> float:
        """Общий тоннаж погруженного багажа за смену."""
        return self._tons_loaded

    def perform_duty(self) -> str:
        """Осуществляет погрузку чемоданов в трюм или на тележку."""
        self._tons_loaded += 0.5
        equipment = "с помощью погрузчика" if self.heavy_machinery_license else "вручную"
        return f"Грузчик {self.full_name} переместил багаж {equipment}."