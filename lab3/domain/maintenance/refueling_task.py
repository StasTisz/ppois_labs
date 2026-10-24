"""Модуль технологической задачи заправки судна авиакеросином."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.fleet.fuel_truck import FuelTruck


class RefuelingTask(ServiceTask):
    """Задача заправки воздушного судна керосином с использованием спецтехники."""

    FUEL_RATE_PER_MINUTE: float = 200.0
    BASE_SETUP_MINUTES: int = 10

    def __init__(
        self,
        aircraft: Aircraft,
        fuel_truck: FuelTruck,
        fuel_amount: float,
        task_code: str = "",
    ) -> None:
        """Инициализирует экземпляр класса RefuelingTask."""
        super().__init__(aircraft, task_code=task_code)
        self.fuel_truck = fuel_truck
        self.fuel_amount = fuel_amount

    def validate_prerequisites(self) -> bool:
        """Проверяет готовность топливозаправщика и самолета к процедуре заправки."""
        return (
            super().validate_prerequisites()
            and self.fuel_truck.current_fuel >= self.fuel_amount
        )

    def calculate_estimated_duration_minutes(self) -> int:
        """Рассчитывает необходимое время заправки исходя из объема керосина."""
        return (
            int(self.fuel_amount / self.FUEL_RATE_PER_MINUTE) + self.BASE_SETUP_MINUTES
        )

    def execute(self) -> str:
        """Использует переданный топливозаправщик для перекачки топлива."""
        self._start()
        self.fuel_truck.refuel_aircraft(self.aircraft, self.fuel_amount)
        self._complete()
        return (
            f"Борт {self.aircraft.tail_number} заправлен на {self.fuel_amount} л. "
            f"через заправщик {self.fuel_truck.license_plate}."
        )
