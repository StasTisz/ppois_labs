from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.fleet.fuel_truck import FuelTruck


class RefuelingTask(ServiceTask):
    def __init__(
        self,
        aircraft: Aircraft,
        fuel_truck: FuelTruck,
        fuel_amount: float,
        task_code: str = "",
    ) -> None:
        super().__init__(aircraft, task_code=task_code)
        self.fuel_truck = fuel_truck
        self.fuel_amount = fuel_amount

    def validate_prerequisites(self) -> bool:
        return (
            super().validate_prerequisites()
            and self.fuel_truck.current_fuel >= self.fuel_amount
        )

    def calculate_estimated_duration_minutes(self) -> int:
        return int(self.fuel_amount / 200.0) + 10

    def execute(self) -> str:
        self._start()
        self.fuel_truck.refuel_aircraft(self.aircraft, self.fuel_amount)
        self._complete()
        return (
            f"Борт {self.aircraft.tail_number} заправлен на {self.fuel_amount} л. "
            f"через заправщик {self.fuel_truck.license_plate}."
        )
