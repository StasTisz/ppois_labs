from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class Airline:
    def __init__(self, name: str, iata_code: str) -> None:
        self.name = name
        self.iata_code = iata_code
        self._fleet: list[Aircraft] = []

    @property
    def fleet_size(self) -> int:
        return len(self._fleet)

    @property
    def fleet(self) -> list[Aircraft]:
        return list(self._fleet)

    def register_aircraft(self, aircraft: Aircraft) -> None:
        if aircraft not in self._fleet:
            self._fleet.append(aircraft)

    def remove_aircraft(self, aircraft: Aircraft) -> None:
        if aircraft in self._fleet:
            self._fleet.remove(aircraft)

    def get_fleet(self) -> list[Aircraft]:
        return list(self._fleet)

    def __repr__(self) -> str:
        return f"Airline(name={self.name!r}, iata={self.iata_code!r}, fleet={len(self._fleet)})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Airline):
            return NotImplemented
        return self.iata_code == other.iata_code

    def __hash__(self) -> int:
        return hash(self.iata_code)
