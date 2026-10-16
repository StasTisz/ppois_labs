"""Модуль перронного автобуса для доставки пассажиров."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class PassengerBus(GroundVehicle):
    """Перронный автобус. Осуществляет трансфер пассажиров к трапу самолета."""

    def __init__(
        self,
        model: str,
        max_speed: float,
        license_plate: str,
        passenger_capacity: int = 100,
        capacity: int | None = None,
    ) -> None:
        """Инициализирует экземпляр класса PassengerBus."""
        super().__init__(model, max_speed, license_plate)
        self.passenger_capacity = (
            capacity if capacity is not None else passenger_capacity
        )
        self._current_passengers = 0
        self.doors_pneumatics_checked = False

    @property
    def passengers_count(self) -> int:
        """Текущее количество пассажиров в салоне."""
        return self._current_passengers

    def board(self, count: int) -> None:
        """Загружает пассажиров в салон автобуса."""
        if count <= 0:
            raise ValueError("Число входящих пассажиров должно быть положительным.")
        if self._current_passengers + count > self.passenger_capacity:
            raise CapacityExceededException(
                f"Автобус {self.license_plate} переполнен (максимум: {self.passenger_capacity} чел.)."
            )
        self._current_passengers += count

    def board_passenger(self, passenger: Passenger) -> None:
        """Осуществляет посадку пассажира в перронный автобус."""
        self.board(1)

    def drop_off(self) -> int:
        """Высаживает пассажиров у трапа или терминала."""
        dropped = self._current_passengers
        self._current_passengers = 0
        return dropped

    def perform_maintenance(self) -> None:
        """ТО автобуса: ревизия пневматики дверей и аппарелей."""
        self.doors_pneumatics_checked = True
        self.requires_maintenance = False
