"""Модуль сервисной задачи уборки пассажирского салона судна."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class CleaningTask(ServiceTask):
    """Уборка салона после высадки пассажиров."""

    DEEP_CLEANING_DURATION_MINUTES: int = 45
    STANDARD_CLEANING_DURATION_MINUTES: int = 20

    def __init__(
        self,
        aircraft: Aircraft,
        requires_deep_cleaning: bool = False,
        cleaning_agent_type: str = "standard",
        task_code: str = "",
    ) -> None:
        """Инициализирует экземпляр класса CleaningTask."""
        super().__init__(aircraft, task_code=task_code)
        self.requires_deep_cleaning = requires_deep_cleaning
        self.cleaning_agent_type = cleaning_agent_type
        self.sanitized: bool = False

    def calculate_estimated_duration_minutes(self) -> int:
        """Рассчитывает расчетную длительность уборки салона самолета."""
        return (
            self.DEEP_CLEANING_DURATION_MINUTES
            if self.requires_deep_cleaning
            else self.STANDARD_CLEANING_DURATION_MINUTES
        )

    def execute(self) -> str:
        """Проводит стандартную или генеральную уборку борта."""
        self._start()
        cleaning_type = "Генеральная" if self.requires_deep_cleaning else "Стандартная"
        self.aircraft.clean()
        self._complete()
        return f"{cleaning_type} уборка салона {self.aircraft.tail_number} выполнена."
