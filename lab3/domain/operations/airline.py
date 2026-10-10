from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Airline:
    def __init__(self, name: str, iata_code: str) -> None:
        self.airline_id = str(uuid.uuid4())
        self.name = name
        self.iata_code = iata_code
        self._fleet: list[Aircraft] = []

    def register_aircraft(self, aircraft: Aircraft) -> None:
        self._fleet.append(aircraft)

    @property
    def fleet_size(self) -> int:
        return len(self._fleet)

    def get_fleet(self) -> list[Aircraft]:
        return self._fleet.copy()
