from __future__ import annotations

from lab3.domain.fleet.aircraft import Aircraft


class PrivateJet(Aircraft):
    def __init__(
        self,
        model: str,
        max_speed: float,
        tail_number: str,
        fuel_capacity: float,
        owner_name: str,
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.owner_name = owner_name
        self.vip_catering_ordered = False
        self.satellite_comms_calibrated = False

    @property
    def is_vip_catered(self) -> bool:
        return self.vip_catering_ordered

    @is_vip_catered.setter
    def is_vip_catered(self, val: bool) -> None:
        self.vip_catering_ordered = val

    def order_vip_catering(self) -> None:
        self.vip_catering_ordered = True

    def request_vip_slot(self, departure_priority: int = 1) -> str:
        return f"VIP-слот (приоритет {departure_priority}) подтвержден для борта {self.tail_number} ({self.owner_name})."

    def perform_maintenance(self) -> None:
        self.satellite_comms_calibrated = True
        self.requires_maintenance = False
