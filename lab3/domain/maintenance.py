import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import TYPE_CHECKING

from lab3.domain.exceptions import MaintenanceRequiredException, WeatherWarningException

if TYPE_CHECKING:
    from lab3.domain.fleet import Aircraft, FuelTruck
    from lab3.domain.people import Employee


class WeatherReport:
    """
    Метеорологическая сводка аэропорта.

    Attributes:
        temperature_c (float): Температура в градусах Цельсия.
        wind_speed_ms (float): Скорость ветра в м/с.
        visibility_m (float): Видимость в метрах.
        is_stormy (bool): Наличие грозового фронта.
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
        """Определяет, безопасны ли погодные условия для взлета/посадки и перронных работ."""
        if self.is_stormy:
            return False
        if self.wind_speed_ms > 25.0:  # Штормовой ветер
            return False
        if self.visibility_m < 400.0:  # Сильный туман
            return False
        return True


class ServiceTask(ABC):
    """
    Базовый абстрактный класс для регламентных задач по обслуживанию борта.

    Attributes:
        task_id (str): UUID задачи.
        aircraft (Aircraft): Воздушное судно, требующее обслуживания.
        status (str): Текущий статус задачи (Pending, InProgress, Completed).
        assigned_staff (list[Employee]): Назначенный на задачу персонал.
    """

    def __init__(self, aircraft: 'Aircraft') -> None:
        self.task_id = str(uuid.uuid4())
        self.aircraft = aircraft
        self.status = "Pending"
        self.assigned_staff: list['Employee'] = []

    def assign_staff(self, employee: 'Employee') -> None:
        """Назначает сотрудника на выполнение задачи."""
        self.assigned_staff.append(employee)

    def _start(self) -> None:
        """Внутренний метод проверки и старта задачи."""
        if not self.assigned_staff:
            raise ValueError("Невозможно начать обслуживание: не назначен персонал.")
        self.status = "InProgress"

    def _complete(self) -> None:
        """Внутренний метод успешного завершения задачи."""
        self.status = "Completed"

    @abstractmethod
    def execute(self) -> str:
        """
        Полиморфный метод выполнения конкретной работы.
        """
        pass


class MaintenanceInspection(ServiceTask):
    """
    Технический осмотр (Line Maintenance) перед вылетом.
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
    Задача заправки воздушного судна керосином.
    """

    def __init__(self, aircraft: 'Aircraft', fuel_truck: 'FuelTruck', fuel_amount: float) -> None:
        super().__init__(aircraft)
        self.fuel_truck = fuel_truck
        self.fuel_amount = fuel_amount

    def execute(self) -> str:
        """Использует топливозаправщик для перекачки керосина."""
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

    def __init__(self, aircraft: 'Aircraft', requires_deep_cleaning: bool = False) -> None:
        super().__init__(aircraft)
        self.requires_deep_cleaning = requires_deep_cleaning

    def execute(self) -> str:
        self._start()

        cleaning_type = "Генеральная" if self.requires_deep_cleaning else "Стандартная"

        self._complete()
        return f"{cleaning_type} уборка салона {self.aircraft.tail_number} выполнена."


class CateringTask(ServiceTask):
    """
    Погрузка бортового питания (кейтеринг).
    """

    def __init__(self, aircraft: 'Aircraft', meals_count: int, includes_vip: bool = False) -> None:
        super().__init__(aircraft)
        self.meals_count = meals_count
        self.includes_vip = includes_vip

    def execute(self) -> str:
        self._start()

        # Если борт — частный джет и требуется VIP-питание, активируем флаг
        if self.includes_vip and hasattr(self.aircraft, 'order_vip_catering'):
            self.aircraft.order_vip_catering()

        self._complete()
        return f"На борт {self.aircraft.tail_number} загружено {self.meals_count} порций питания."