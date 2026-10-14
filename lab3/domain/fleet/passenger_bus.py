from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class PassengerBus(GroundVehicle):
    def __init__(
        self,
        model: str,
        max_speed: float,
        license_plate: str,
        passenger_capacity: int = 100,
        capacity: int | None = None,
    ) -> None:
        super().__init__(model, max_speed, license_plate)
        self.passenger_capacity = (
            capacity if capacity is not None else passenger_capacity
        )
        self._current_passengers = 0
        self.doors_pneumatics_checked = False

    @property
    def passengers_count(self) -> int:
        return self._current_passengers

    def board(self, count: int) -> None:
        if count <= 0:
            raise ValueError("Число входящих пассажиров должно быть положительным.")
        if self._current_passengers + count > self.passenger_capacity:
            raise CapacityExceededException(
                f"Автобус {self.license_plate} переполнен (максимум: {self.passenger_capacity} чел.)."
            )
        self._current_passengers += count

    def board_passenger(self, passenger: Passenger) -> None:
        self.board(1)

    def drop_off(self) -> int:
        dropped = self._current_passengers
        self._current_passengers = 0
        return dropped

    def perform_maintenance(self) -> None:
        self.doors_pneumatics_checked = True
        self.requires_maintenance = False
