from __future__ import annotations

from lab3.domain.exceptions import CapacityExceededException


class ParkingLot:
    def __init__(
        self, zone_code: str, total_spaces: int = 100, capacity: int | None = None
    ) -> None:
        self.zone_code = zone_code
        self.total_spaces = capacity if capacity is not None else total_spaces
        self._parked_cars: list[str] = []
        self._parked_cars_count = 0

    @property
    def available_spaces(self) -> int:
        return self.total_spaces - len(self._parked_cars)

    def park_car(self, license_plate: str = "") -> None:
        if len(self._parked_cars) >= self.total_spaces:
            raise CapacityExceededException(
                f"Парковка зоны '{self.zone_code}' заполнена (максимум {self.total_spaces} авто)."
            )
        self._parked_cars.append(license_plate)
        self._parked_cars_count = len(self._parked_cars)

    def remove_car(self, license_plate: str = "") -> None:
        if license_plate and license_plate in self._parked_cars:
            self._parked_cars.remove(license_plate)
        elif self._parked_cars:
            self._parked_cars.pop()
        self._parked_cars_count = len(self._parked_cars)

    def __repr__(self) -> str:
        return f"ParkingLot(zone={self.zone_code!r}, parked={self._parked_cars_count}/{self.total_spaces})"
