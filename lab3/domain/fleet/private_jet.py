"""Модуль частного самолета деловой авиации (бизнес-джета)."""

from __future__ import annotations

from lab3.domain.fleet.aircraft import Aircraft


class PrivateJet(Aircraft):
    """Частный бизнес-джет. Включает сервисы VIP-кейтеринга и спутниковую связь."""

    def __init__(
        self,
        model: str,
        max_speed: float,
        tail_number: str,
        fuel_capacity: float,
        owner_name: str,
    ) -> None:
        """Инициализирует экземпляр класса PrivateJet."""
        super().__init__(model, max_speed, tail_number, fuel_capacity)
        self.owner_name = owner_name
        self.vip_catering_ordered = False
        self.satellite_comms_calibrated = False

    @property
    def is_vip_catered(self) -> bool:
        """Возвращает признак vip_catered."""
        return self.vip_catering_ordered

    @is_vip_catered.setter
    def is_vip_catered(self, val: bool) -> None:
        """Устанавливает значение атрибута is_vip_catered."""
        self.vip_catering_ordered = val

    def order_vip_catering(self) -> None:
        """Заказывает премиальное бортовое питание."""
        self.vip_catering_ordered = True

    def request_vip_slot(self, departure_priority: int = 1) -> str:
        """Запрашивает выделенный VIP-слот обслуживания частного бизнес-джета."""
        return f"VIP-слот (приоритет {departure_priority}) подтвержден для борта {self.tail_number} ({self.owner_name})."

    def perform_maintenance(self) -> None:
        """ТО бизнес-джета: калибровка спутниковой связи."""
        self.satellite_comms_calibrated = True
        self.requires_maintenance = False
