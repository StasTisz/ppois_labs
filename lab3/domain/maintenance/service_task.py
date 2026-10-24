"""Модуль базовой регламентной сервисной операции наземного обслуживания."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft
    from lab3.domain.people.employee import Employee


class ServiceTask(ABC):
    """Базовый абстрактный класс для регламентных задач по обслуживанию борта.
    Управляет статусом выполнения и привязкой сотрудников."""

    def __init__(self, aircraft: Aircraft, task_code: str = "") -> None:
        """Инициализирует экземпляр класса ServiceTask."""
        self.task_code = task_code or f"TASK-{aircraft.tail_number}"
        self.aircraft = aircraft
        self._status = "Pending"
        self._assigned_staff: list[Employee] = []

    @property
    def status(self) -> str:
        """Текущий статус выполнения задачи (только чтение)."""
        return self._status

    @property
    def assigned_staff(self) -> list[Employee]:
        """Безопасная копия списка назначенного персонала."""
        return list(self._assigned_staff)

    def assign_staff(self, employee: Employee) -> None:
        """Назначает сотрудника на выполнение данной задачи."""
        self._assigned_staff.append(employee)

    def validate_prerequisites(self) -> bool:
        """Проверяет необходимые технические условия перед началом сервисных работ."""
        return len(self._assigned_staff) > 0

    def calculate_estimated_duration_minutes(self) -> int:
        """Возвращает нормативную продолжительность выполнения задачи."""
        return 30

    def _start(self) -> None:
        """Внутренний метод валидации и старта задачи."""
        if not self.validate_prerequisites():
            raise ValueError("Невозможно начать обслуживание: не назначен персонал.")
        self._status = "InProgress"

    def _complete(self) -> None:
        """Внутренний метод успешного закрытия задачи."""
        self._status = "Completed"

    @abstractmethod
    def execute(self) -> str:
        """Полиморфный контракт выполнения работы."""
