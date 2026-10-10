from __future__ import annotations

from lab3.domain.maintenance.service_task import ServiceTask


class MaintenanceInspection(ServiceTask):
    def execute(self) -> str:
        self._start()
        self.aircraft.perform_maintenance()
        self._complete()
        return f"Технический осмотр борта {self.aircraft.tail_number} успешно завершен."
