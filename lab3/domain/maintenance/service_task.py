from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.people.employee import Employee


class ServiceTask(ABC):
    def __init__(self, aircraft: Aircraft) -> None:
        self.task_id = str(uuid.uuid4())
        self.aircraft = aircraft
        self._status = "Pending"
        self._assigned_staff: list[Employee] = []

    @property
    def status(self) -> str:
        return self._status

    @property
    def assigned_staff(self) -> list[Employee]:
        return self._assigned_staff.copy()

    def assign_staff(self, employee: Employee) -> None:
        self._assigned_staff.append(employee)

    def _start(self) -> None:
        if not self._assigned_staff:
            raise ValueError("Невозможно начать обслуживание: не назначен персонал.")
        self._status = "InProgress"

    def _complete(self) -> None:
        self._status = "Completed"

    @abstractmethod
    def execute(self) -> str:
        """Полиморфный контракт выполнения работы."""
