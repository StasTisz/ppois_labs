"""
Модуль безопасности и контроля аэропорта.

Отвечает за досмотр пассажиров и багажа (Служба авиационной безопасности),
проверку виз (Пограничный контроль) и таможенных деклараций (Таможня).
Обеспечивает валидацию прохождения контроля с помощью оборудования (сканеров)
и выброс соответствующих доменных исключений при нарушениях.
"""

from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from lab3.domain.exceptions import SecurityCheckFailedException, VisaExpiredException

# Отложенный импорт для строгой типизации методов (замена Any)
if TYPE_CHECKING:
    from lab3.domain.operations import Baggage
    from lab3.domain.people import Passenger, SecurityOfficer


class Visa:
    """
    Виза для пересечения границы.

    Attributes:
        visa_id (str): Внутренний идентификатор визы.
        country (str): Страна, выдавшая визу.
        expiration_date (datetime): Срок окончания действия.
    """

    def __init__(self, country: str, expiration_date: datetime) -> None:
        self.visa_id = str(uuid.uuid4())
        self.country = country
        self.expiration_date = expiration_date

    def is_valid(self, current_date: datetime) -> bool:
        """Проверяет, не истек ли срок действия визы на указанную дату."""
        return current_date <= self.expiration_date


class CustomsDeclaration:
    """
    Таможенная декларация на провоз товаров или валюты.

    Attributes:
        declaration_id (str): Уникальный номер декларации.
        passenger_id (str): Идентификатор декларанта.
        declared_items (list[str]): Список задекларированных вещей (например, "Дрон").
        cash_amount (float): Сумма провозимых наличных в USD.
    """

    def __init__(self, passenger_id: str, declared_items: list[str], cash_amount: float) -> None:
        self.declaration_id = str(uuid.uuid4())
        self.passenger_id = passenger_id
        self.declared_items = declared_items
        self.cash_amount = cash_amount
        self._is_approved = False

    @property
    def is_approved(self) -> bool:
        """Статус одобрения таможней (только чтение)."""
        return self._is_approved

    def approve(self) -> None:
        """Ставит официальную отметку таможни о прохождении контроля."""
        self._is_approved = True


class Scanner(ABC):
    """
    Базовый абстрактный класс для оборудования службы безопасности.
    """

    def __init__(self, model: str) -> None:
        self.scanner_id = str(uuid.uuid4())
        self.model = model
        self.is_active = True

    @abstractmethod
    def scan(self, target: Passenger | Baggage | None) -> bool:
        """
        Полиморфный метод сканирования объекта.
        Возвращает True, если запрещенных предметов не найдено.
        """
        pass


class MetalDetector(Scanner):
    """
    Рамочный металлодетектор для досмотра людей.
    """

    def scan(self, target: Passenger | Baggage | None) -> bool:
        """Анализирует наличие металла у пассажира."""
        if not self.is_active:
            raise ValueError(f"Детектор {self.model} выключен.")
        # В реальной бизнес-логике здесь была бы проверка свойств объекта Passenger
        return True


class XRayScanner(Scanner):
    """
    Рентгеновский интроскоп для досмотра ручной клади и багажа.
    """

    def scan(self, target: Passenger | Baggage | None) -> bool:
        """Просвечивает багаж на наличие запрещенных к перевозке веществ."""
        if not self.is_active:
            raise ValueError(f"Интроскоп {self.model} выключен.")
        # В реальной бизнес-логике здесь была бы проверка содержимого Baggage
        return True


class SecurityCheckpoint:
    """
    Зона предполетного досмотра (САБ - служба авиационной безопасности).
    """

    def __init__(self, number: int) -> None:
        self.checkpoint_id = str(uuid.uuid4())
        self.number = number
        self.metal_detector: MetalDetector | None = None
        self.xray_scanner: XRayScanner | None = None
        self.officer: SecurityOfficer | None = None

    def assign_equipment(self, metal_detector: MetalDetector, xray_scanner: XRayScanner) -> None:
        """Комплектует пункт досмотра необходимым оборудованием."""
        self.metal_detector = metal_detector
        self.xray_scanner = xray_scanner

    def assign_officer(self, officer: SecurityOfficer) -> None:
        """Назначает дежурного сотрудника на пункт."""
        self.officer = officer

    def process_passenger(self, passenger: Passenger, carry_on: Baggage | None = None) -> None:
        """
        Осуществляет комплексный досмотр пассажира и его ручной клади.

        Raises:
            ValueError: Если пункт не укомплектован или нет офицера на смене.
            SecurityCheckFailedException: Если досмотр не пройден (сигнал тревоги сканера).
        """
        if not self.metal_detector or not self.xray_scanner:
            raise ValueError(f"Пункт досмотра {self.number} не укомплектован оборудованием.")
        if not self.officer or not self.officer.is_on_shift:
            raise ValueError("Нет дежурного офицера для проведения досмотра.")

        person_clear = self.metal_detector.scan(passenger)
        baggage_clear = self.xray_scanner.scan(carry_on) if carry_on else True

        if not person_clear or not baggage_clear:
            raise SecurityCheckFailedException(f"Пассажир {passenger.full_name} не прошел досмотр СБ.")


class PassportControl:
    """
    Пограничный контроль (проверка документов и виз).
    """

    def __init__(self, booth_number: int) -> None:
        self.booth_id = str(uuid.uuid4())
        self.booth_number = booth_number

    def check_documents(self, passenger: Passenger, visa: Visa | None, destination_country: str) -> None:
        """
        Проверяет легальность выезда/въезда по паспорту и визе.

        Raises:
            VisaExpiredException: При отсутствии, несоответствии страны или просрочке визы.
        """
        if not visa:
            raise VisaExpiredException(f"Отсутствует виза для въезда в страну {destination_country}.")

        if visa.country != destination_country:
            raise VisaExpiredException(f"В паспорте виза {visa.country}, требуется виза {destination_country}.")

        if not visa.is_valid(datetime.now()):
            raise VisaExpiredException("Срок действия визы истек.")


class CustomsControl:
    """
    Таможенный контроль. Проверяет соблюдение лимитов на вывоз валюты.
    """
    MAX_CASH_ALLOWED_USD = 10000.0

    def __init__(self) -> None:
        self.control_id = str(uuid.uuid4())

    def inspect_declaration(self, declaration: CustomsDeclaration) -> None:
        """
        Проверяет таможенную декларацию и одобряет её, если нет нарушений.

        Raises:
            SecurityCheckFailedException: При превышении лимита провозимых наличных.
        """
        if declaration.cash_amount > self.MAX_CASH_ALLOWED_USD:
            raise SecurityCheckFailedException(
                f"Сумма {declaration.cash_amount}$ превышает лимит вывоза "
                f"без дополнительных разрешений ({self.MAX_CASH_ALLOWED_USD}$)."
            )
        declaration.approve()