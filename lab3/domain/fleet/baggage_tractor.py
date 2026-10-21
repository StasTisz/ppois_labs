"""Модуль перронного багажного тягача."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle

if TYPE_CHECKING:
    from lab3.domain.operations.baggage import Baggage


class BaggageTractor(GroundVehicle):
    """Багажный тягач. Перевозит тележки с чемоданами между терминалом и бортом."""

    def __init__(
        self,
        model: str,
        max_speed: float,
        license_plate: str,
        max_carts: int = 4,
    ) -> None:
        """Инициализирует экземпляр класса BaggageTractor."""
        super().__init__(model, max_speed, license_plate)
        self.max_carts = max_carts
        self._current_carts = 0
        self.tow_hitch_greased = False

    @property
    def current_carts(self) -> int:
        """Текущее количество прицепленных тележек."""
        return self._current_carts

    def attach_cart(self) -> None:
        """Прицепляет дополнительную багажную тележку."""
        if self._current_carts >= self.max_carts:
            raise CapacityExceededException(
                f"Тягач {self.license_plate} не может везти более {self.max_carts} тележек."
            )
        self._current_carts += 1

    def transport_baggage(self, baggage: Baggage) -> None:
        """Транспортирует проверенный багаж между терминалом и стоянкой самолета."""
        baggage.check_weight()
        self.attach_cart()

    def detach_all_carts(self) -> None:
        """Отцепляет все тележки."""
        self._current_carts = 0

    def perform_maintenance(self) -> None:
        """ТО тягача: смазка сцепки и проверка тормозного контура тележек."""
        self.tow_hitch_greased = True
        self.requires_maintenance = False
