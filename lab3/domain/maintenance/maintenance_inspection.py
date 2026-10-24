"""Модуль предполетного технического осмотра воздушного судна."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class MaintenanceInspection(ServiceTask):
    """Предполетный технический осмотр (Line Maintenance)."""

    ESTIMATED_DURATION_MINUTES: int = 60

    def __init__(
        self,
        aircraft: Aircraft,
        task_code: str = "",
        inspector_license: str = "INSP-001",
    ) -> None:
        """Инициализирует экземпляр класса MaintenanceInspection."""
        super().__init__(aircraft, task_code=task_code)
        self.inspector_license = inspector_license
        self.checklist_passed: bool = False
        self.remarks: list[str] = []

    def add_remark(self, remark: str) -> None:
        """Вносит замечание в технический журнал предполетного осмотра."""
        self.remarks.append(remark)

    def calculate_estimated_duration_minutes(self) -> int:
        """Рассчитывает регламентную продолжительность техосмотра судна."""
        return self.ESTIMATED_DURATION_MINUTES

    def execute(self) -> str:
        """Запускает полиморфный метод perform_maintenance() у самого судна."""
        self._start()
        self.checklist_passed = True
        self.aircraft.perform_maintenance()
        self._complete()
        return f"Технический осмотр борта {self.aircraft.tail_number} успешно завершен."
