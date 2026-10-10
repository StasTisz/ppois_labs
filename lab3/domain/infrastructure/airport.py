from __future__ import annotations

from lab3.domain.infrastructure.control_tower import ControlTower
from lab3.domain.infrastructure.hangar import Hangar
from lab3.domain.infrastructure.parking_lot import ParkingLot
from lab3.domain.infrastructure.terminal import Terminal


class Airport:
    def __init__(self, name: str, iata_code: str) -> None:
        self.name = name
        self.iata_code = iata_code
        self.control_tower = ControlTower()
        self._terminals: list[Terminal] = []
        self._hangars: list[Hangar] = []
        self._parking_lots: list[ParkingLot] = []

    def add_terminal(self, terminal: Terminal) -> None:
        self._terminals.append(terminal)

    def get_terminal(self, name: str) -> Terminal | None:
        for t in self._terminals:
            if t.name == name:
                return t
        return None
