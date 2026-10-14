from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger


class Scanner(ABC):
    def __init__(self, model: str, serial_number: str | None = None) -> None:
        self.serial_number = serial_number or f"SCN-{str(uuid.uuid4())[:8].upper()}"
        self.model = model
        self.is_active = True
        self._is_calibrated = True

    @property
    def scanner_id(self) -> str:
        return self.serial_number

    @property
    def is_calibrated(self) -> bool:
        return self._is_calibrated

    def toggle_power(self) -> None:
        self.is_active = not self.is_active

    def calibrate(self) -> bool:
        if not self.is_active:
            raise ValueError(f"Нельзя откалибровать выключенный сканер {self.model}.")
        self._is_calibrated = True
        return True

    @abstractmethod
    def scan(self, target: Passenger | Baggage | None) -> bool:
        """Полиморфный метод сканирования объекта."""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(model={self.model!r}, active={self.is_active}, serial={self.serial_number!r})"
