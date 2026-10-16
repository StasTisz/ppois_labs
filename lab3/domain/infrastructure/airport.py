"""Модуль предприятия международного аэропорта."""

from __future__ import annotations

from lab3.domain.infrastructure.control_tower import ControlTower
from lab3.domain.infrastructure.hangar import Hangar
from lab3.domain.infrastructure.parking_lot import ParkingLot
from lab3.domain.infrastructure.terminal import Terminal


class Airport:
    """Агрегатор верхнего уровня. Представляет физический аэропорт в целом.
    Объединяет терминалы, парковки, вышку и ангары."""

    def __init__(self, name: str, iata_code: str) -> None:
        """Инициализирует экземпляр класса Airport."""
        self.name = name
        self.iata_code = iata_code
        self.control_tower = ControlTower(f"{name} Tower")
        self.hangar = Hangar(1)
        self.parking_lot = ParkingLot("Main Zone")
        self._terminals: list[Terminal] = []

    @property
    def terminals(self) -> list[Terminal]:
        """Возвращает значение атрибута terminals."""
        return list(self._terminals)

    def add_terminal(self, terminal: Terminal) -> None:
        """Вводит в эксплуатацию новый пассажирский терминал аэропорта."""
        self._terminals.append(terminal)

    def get_terminal(self, name: str) -> Terminal | None:
        """Ищет терминал по его названию (например, 'Terminal 1')."""
        for term in self._terminals:
            if term.name == name:
                return term
        return None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"Airport(name={self.name!r}, code={self.iata_code!r}, terminals={len(self._terminals)})"
