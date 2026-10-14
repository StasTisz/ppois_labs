from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.aircraft import Aircraft


class PassengerAircraft(Aircraft):
    def __init__(
        self,
        model: str,
        max_speed: float,
        tail_number: str,
        fuel_capacity: float,
        seating_capacity: int = 150,
        max_passengers: int | None = None,
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.seating_capacity = (
            max_passengers if max_passengers is not None else seating_capacity
        )
        self._current_passengers = 0
        self.oxygen_masks_tested = False
        self.cabin_pressurization_ok = False

    @property
    def max_passengers(self) -> int:
        return self.seating_capacity

    @property
    def passengers_count(self) -> int:
        return self._current_passengers

    def board_passengers(self, count: int) -> None:
        if count <= 0:
            raise ValueError("Число пассажиров должно быть положительным.")
        if self._current_passengers + count > self.seating_capacity:
            raise CapacityExceededException(
                f"Превышена вместимость салона: {self.seating_capacity} мест."
            )
        self._current_passengers += count

    def disembark_passengers(self) -> int:
        disembarked = self._current_passengers
        self._current_passengers = 0
        return disembarked

    def perform_maintenance(self) -> None:
        self.oxygen_masks_tested = True
        self.cabin_pressurization_ok = True
        self.requires_maintenance = False
