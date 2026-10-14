from __future__ import annotations

from abc import ABC, abstractmethod


class Vehicle(ABC):
    MAX_OPERATING_HOURS_THRESHOLD: float = 500.0

    def __init__(self, model: str, max_speed: float) -> None:
        self.model = model
        self.max_speed = max_speed
        self.requires_maintenance = False
        self.operating_hours = 0.0

    def log_hours(self, hours: float) -> None:
        if hours < 0:
            raise ValueError("Отработанные часы не могут быть отрицательными.")
        self.operating_hours += hours
        if self.operating_hours > self.MAX_OPERATING_HOURS_THRESHOLD:
            self.requires_maintenance = True

    def mark_for_service(self) -> None:
        self.requires_maintenance = True

    @abstractmethod
    def perform_maintenance(self) -> None:
        """Полиморфный контракт проведения ТО."""
