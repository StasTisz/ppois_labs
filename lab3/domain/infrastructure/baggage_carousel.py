from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.operations.flight import Flight


class BaggageCarousel:
    def __init__(self, number: int) -> None:
        self.carousel_id = str(uuid.uuid4())
        self.number = number
        self.is_active = False
        self.assigned_flight: Flight | None = None

    def activate(self, flight: Flight) -> None:
        self.assigned_flight = flight
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False
        self.assigned_flight = None
