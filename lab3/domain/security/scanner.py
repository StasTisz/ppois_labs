from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage
    from lab3.domain.people.passenger import Passenger


class Scanner(ABC):
    def __init__(self, model: str) -> None:
        self.scanner_id = str(uuid.uuid4())
        self.model = model
        self.is_active = True

    @abstractmethod
    def scan(self, target: Passenger | Baggage | None) -> bool:
        """Полиморфный метод сканирования объекта."""
