"""
Модуль сервисного обслуживания и метеоусловий аэропорта.

Отвечает за регламентные работы на перроне: технический осмотр бортов,
дозаправку, уборку салонов и загрузку бортового питания (кейтеринг).
Реализует объектно-ориентированный паттерн «Команда» (Command) через
базовый класс ServiceTask, где каждая задача имеет свой жизненный цикл
и привязанный персонал. Также включает генерацию метеосводок.
"""

from __future__ import annotations
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

# Отложенный импорт защищает от циклических зависимостей,
# позволяя использовать строгую типизацию без ошибок в рантайме.
if TYPE_CHECKING:
    from lab3.domain.fleet import Aircraft, FuelTruck
    from lab3.domain.people import Employee


class WeatherReport:
    """
    Метеорологическая сводка аэропорта.
    Служит источником правды для диспетчерской вышки при выдаче разрешений.

    Attributes:
        report_id (str): Внутренний номер сводки.
        timestamp (datetime): Точное время формирования отчета.
        temperature_c (float): Температура в градусах Цельсия.
        wind_speed_ms (float): Скорость ветра в м/с.
        visibility_m (float): Видимость в метрах.
        is_stormy (bool): Наличие активного грозового фронта.
    """

    def __init__(self, temperature_c: float, wind_speed_ms: float, visibility_m: float, is_stormy: bool) -> None:
        self.report_id = str(uuid.uuid4())
        self.timestamp = datetime.now()
        self.temperature_c = temperature_c
        self.wind_speed_ms = wind_speed_ms
        self.visibility_m = visibility_m
        self.is_stormy = is_stormy

    @property
    def is_safe_for_operations(self) -> bool:
        """
        Анализирует параметры погоды и определяет, безопасны ли условия
        для взлета, посадки и перронных работ.
        """
        if self.is_stormy:
            return False
        if self.wind_speed_ms > 25.0:  # Штормовой ветер
            return False
        if self.visibility_m < 400.0:  # Сильный туман (ниже метеоминимума)
            return False
        return True


class ServiceTask(ABC):
    """
    Базовый абстрактный класс для регламентных задач по обслуживанию борта.
    Управляет статусом выполнения и привязкой сотрудников.

    Attributes:
        task_id (str): UUID задачи.
        aircraft (Aircraft): Воздушное судно, требующее обслуживания.
    """

    def __init__(self, aircraft: Aircraft) -> None:
        self.task_id = str(uuid.uuid4())
        self.aircraft = aircraft
        self._status = "Pending"  # Pending, InProgress, Completed
        self._assigned_staff: list[Employee] = []

    @property
    def status(self) -> str:
        """Текущий статус выполнения задачи (только чтение)."""
        return self._status

    @property
    def assigned_staff(self) -> list[Employee]:
        """Безопасная копия списка назначенного персонала."""
        return self._assigned_staff.copy()

    def assign_staff(self, employee: Employee) -> None:
        """
        Назначает сотрудника на выполнение данной задачи.
        """
        self._assigned_staff.append(employee)

    def _start(self) -> None:
        """Внутренний метод валидации и старта задачи."""
        if not self._assigned_staff:
            raise ValueError("Невозможно начать обслуживание: не назначен персонал.")
        self._status = "InProgress"

    def _complete(self) -> None:
        """Внутренний метод успешного закрытия задачи."""
        self._status = "Completed"

    @abstractmethod
    def execute(self) -> str:
        """
        Полиморфный контракт выполнения конкретной работы.
        Обязателен для переопределения в дочерних классах обслуживания.
        """
        pass


class MaintenanceInspection(ServiceTask):
    """
    Предполетный технический осмотр (Line Maintenance).
    """

    def execute(self) -> str:
        """Запускает полиморфный метод perform_maintenance() у самого судна."""
        self._start()

        # Делегируем логику самому объекту Aircraft
        self.aircraft.perform_maintenance()

        self._complete()
        return f"Технический осмотр борта {self.aircraft.tail_number} успешно завершен."


class RefuelingTask(ServiceTask):
    """
    Задача заправки воздушного судна керосином с использованием спецтехники.
    """

    def __init__(self, aircraft: Aircraft, fuel_truck: FuelTruck, fuel_amount: float) -> None:
        super().__init__(aircraft)
        self.fuel_truck = fuel_truck
        self.fuel_amount = fuel_amount

    def execute(self) -> str:
        """Использует переданный топливозаправщик для перекачки топлива."""
        self._start()

        # Вызываем метод спецтехники, который инкапсулирует логику заправки
        self.fuel_truck.refuel_aircraft(self.aircraft, self.fuel_amount)

        self._complete()
        return (
            f"Борт {self.aircraft.tail_number} заправлен на {self.fuel_amount} л. "
            f"через заправщик {self.fuel_truck.license_plate}."
        )


class CleaningTask(ServiceTask):
    """
    Уборка салона после высадки пассажиров.
    """

    def __init__(self, aircraft: Aircraft, requires_deep_cleaning: bool = False) -> None:
        super().__init__(aircraft)
        self.requires_deep_cleaning = requires_deep_cleaning

    def execute(self) -> str:
        """Проводит стандартную или генеральную уборку борта."""
        self._start()

        cleaning_type = "Генеральная" if self.requires_deep_cleaning else "Стандартная"

        self._complete()
        return f"{cleaning_type} уборка салона {self.aircraft.tail_number} выполнена."


class CateringTask(ServiceTask):
    """
    Погрузка бортового питания (кейтеринг).
    """

    def __init__(self, aircraft: Aircraft, meals_count: int, includes_vip: bool = False) -> None:
        super().__init__(aircraft)
        self.meals_count = meals_count
        self.includes_vip = includes_vip

    def execute(self) -> str:
        """Осуществляет загрузку питания в кухонные блоки судна."""
        self._start()

        # Если борт — частный джет и требуется VIP-питание, активируем флаг через duck typing
        if self.includes_vip and hasattr(self.aircraft, 'order_vip_catering'):
            self.aircraft.order_vip_catering()

        self._complete()
        return f"На борт {self.aircraft.tail_number} загружено {self.meals_count} порций питания."