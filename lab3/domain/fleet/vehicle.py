from __future__ import annotations

import uuid
from abc import ABC, abstractmethod


class Vehicle(ABC):
    def __init__(self, model: str, max_speed: float) -> None:
        self.vehicle_id = str(uuid.uuid4())
        self.model = model
        self.max_speed = max_speed
        self.requires_maintenance = False
        self.operating_hours = 0.0

    @abstractmethod
    def perform_maintenance(self) -> None:
        """Полиморфный контракт проведения ТО."""
