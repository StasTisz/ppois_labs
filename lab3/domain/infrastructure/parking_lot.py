"""Модуль стоянки воздушных судов или автотранспорта."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException

if TYPE_CHECKING:
    from lab3.domain.fleet.ground_vehicle import GroundVehicle


class ParkingLot:
    """Паркинг для автомобилей клиентов и сотрудников аэропорта."""

    def __init__(
        self, zone_code: str, total_spaces: int = 100, capacity: int | None = None
    ) -> None:
        """Инициализирует экземпляр класса ParkingLot."""
        self.zone_code = zone_code
        self.total_spaces = capacity if capacity is not None else total_spaces
        self._parked_vehicles: list[GroundVehicle] = []

    @property
    def parked_vehicles_count(self) -> int:
        """Возвращает значение атрибута parked_vehicles_count."""
        return len(self._parked_vehicles)

    @property
    def available_spaces(self) -> int:
        """Возвращает значение атрибута available_spaces."""
        return self.total_spaces - len(self._parked_vehicles)

    def park_car(self, vehicle: GroundVehicle) -> None:
        """Осуществляет въезд автомобиля на паркинг."""
        if len(self._parked_vehicles) >= self.total_spaces:
            raise CapacityExceededException(
                f"Парковка зоны '{self.zone_code}' заполнена (максимум {self.total_spaces} авто)."
            )
        self._parked_vehicles.append(vehicle)

    def remove_car(self, vehicle: GroundVehicle | None = None) -> GroundVehicle | None:
        """Освобождает парковочное место."""
        if vehicle and vehicle in self._parked_vehicles:
            self._parked_vehicles.remove(vehicle)
            return vehicle
        elif self._parked_vehicles:
            return self._parked_vehicles.pop()
        return None

    def __repr__(self) -> str:
        """Возвращает отладочное строковое представление объекта."""
        return f"ParkingLot(zone={self.zone_code!r}, parked={len(self._parked_vehicles)}/{self.total_spaces})"
