"""Модуль сервисной задачи обеспечения рейса бортпитанием."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.maintenance.service_task import ServiceTask

if TYPE_CHECKING:
    from lab3.domain.fleet.aircraft import Aircraft


class CateringTask(ServiceTask):
    """Погрузка бортового питания (кейтеринг)."""

    VIP_DURATION_MINUTES: int = 30
    STANDARD_DURATION_MINUTES: int = 15

    def __init__(
        self,
        aircraft: Aircraft,
        meals_count: int,
        includes_vip: bool = False,
        task_code: str = "",
    ) -> None:
        """Инициализирует экземпляр класса CateringTask."""
        super().__init__(aircraft, task_code=task_code)
        self.meals_count = meals_count
        self.includes_vip = includes_vip

    def calculate_estimated_duration_minutes(self) -> int:
        """Рассчитывает плановое время доставки и загрузки бортпитания."""
        return (
            self.VIP_DURATION_MINUTES
            if self.includes_vip
            else self.STANDARD_DURATION_MINUTES
        )

    def execute(self) -> str:
        """Осуществляет загрузку питания в кухонные блоки судна."""
        self._start()
        if self.includes_vip and hasattr(self.aircraft, "order_vip_catering"):
            self.aircraft.order_vip_catering()
        self._complete()
        return f"На борт {self.aircraft.tail_number} загружено {self.meals_count} порций питания."
