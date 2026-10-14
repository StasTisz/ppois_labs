from __future__ import annotations

from lab3.domain.fleet.vehicle import Vehicle


class GroundVehicle(Vehicle):
    def __init__(self, model: str, max_speed: float, license_plate: str) -> None:
        super().__init__(model, max_speed)
        self.license_plate = license_plate
        self.is_dispatched = False

    @property
    def is_available(self) -> bool:
        return not self.is_dispatched

    def dispatch(self) -> None:
        if self.is_dispatched:
            raise ValueError(
                f"Транспорт {self.license_plate} уже отправлен на задание."
            )
        self.is_dispatched = True

    def release(self) -> None:
        self.is_dispatched = False

    def perform_maintenance(self) -> None:
        self.requires_maintenance = False

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(plate={self.license_plate!r}, model={self.model!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GroundVehicle):
            return NotImplemented
        return self.license_plate == other.license_plate

    def __hash__(self) -> int:
        return hash(self.license_plate)
