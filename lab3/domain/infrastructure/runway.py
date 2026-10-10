from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from lab3.domain.exceptions import RunwayBusyException

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Runway:
    def __init__(self, number: str, length: int) -> None:
        self.runway_id = str(uuid.uuid4())
        self.number = number
        self.length = length
        self.is_busy = False
        self.current_aircraft: Aircraft | None = None

    def occupy(self, aircraft: Aircraft) -> None:
        if self.is_busy:
            raise RunwayBusyException(f"Полоса {self.number} уже занята.")
        self.is_busy = True
        self.current_aircraft = aircraft

    def clear(self) -> None:
        self.is_busy = False
        self.current_aircraft = None
