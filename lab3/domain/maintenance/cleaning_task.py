from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class CleaningTask(ServiceTask):
    def __init__(self, aircraft: Aircraft, requires_deep_cleaning: bool = False) -> None:
        super().__init__(aircraft)
        self.requires_deep_cleaning = requires_deep_cleaning

    def execute(self) -> str:
        self._start()
        cleaning_type = "Генеральная" if self.requires_deep_cleaning else "Стандартная"
        self._complete()
        return f"{cleaning_type} уборка салона {self.aircraft.tail_number} выполнена."
