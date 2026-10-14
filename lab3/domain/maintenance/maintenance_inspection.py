from __future__ import annotations

from lab3.domain.maintenance.service_task import ServiceTask


class MaintenanceInspection(ServiceTask):
    def calculate_estimated_duration_minutes(self) -> int:
        return 60

    def execute(self) -> str:
        self._start()
        self.aircraft.perform_maintenance()
        self._complete()
        return f"Технический осмотр борта {self.aircraft.tail_number} успешно завершен."
