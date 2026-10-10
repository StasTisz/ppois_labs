from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.aircraft import Aircraft


class PassengerAircraft(Aircraft):
    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, max_passengers: int
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.max_passengers = max_passengers
        self._passengers_count = 0
        self.oxygen_masks_tested = False
        self.cabin_pressurization_ok = True

    @property
    def passengers_count(self) -> int:
        return self._passengers_count

    def board_passengers(self, count: int) -> None:
        if self._passengers_count + count > self.max_passengers:
            raise CapacityExceededException("Количество пассажиров превышает вместимость салона.")
        self._passengers_count += count

    def disembark_passengers(self) -> int:
        count = self._passengers_count
        self._passengers_count = 0
        return count

    def perform_maintenance(self) -> None:
        self.oxygen_masks_tested = True
        self.cabin_pressurization_ok = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
