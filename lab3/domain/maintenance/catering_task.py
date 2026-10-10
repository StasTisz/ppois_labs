from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class CateringTask(ServiceTask):
    def __init__(self, aircraft: Aircraft, meals_count: int, includes_vip: bool = False) -> None:
        super().__init__(aircraft)
        self.meals_count = meals_count
        self.includes_vip = includes_vip

    def execute(self) -> str:
        self._start()
        if self.includes_vip and hasattr(self.aircraft, "order_vip_catering"):
            self.aircraft.order_vip_catering()
        self._complete()
        return f"На борт {self.aircraft.tail_number} загружено {self.meals_count} порций питания."
