from __future__ import annotations

from lab3.domain.fleet.aircraft import Aircraft


class PrivateJet(Aircraft):
    def __init__(
            self, model: str, max_speed: float, tail_number: str,
            fuel_capacity: float, owner_name: str
    ) -> None:
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.owner_name = owner_name
        self.is_vip_catered = False
        self.satellite_comms_calibrated = False

    def order_vip_catering(self) -> None:
        self.is_vip_catered = True

    def perform_maintenance(self) -> None:
        self.satellite_comms_calibrated = True
        self.requires_maintenance = False
        self.operating_hours = 0.0
