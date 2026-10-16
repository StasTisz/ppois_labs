"""Модуль пилота воздушного судна."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.crew_member import CrewMember

if TYPE_CHECKING:
    from lab3.domain.operations.flight_plan import FlightPlan


class Pilot(CrewMember):
    """Пилот воздушного судна."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        license_type: str,
        is_captain: bool = False,
    ) -> None:
        """Инициализирует экземпляр класса Pilot."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.license_type = license_type
        self.is_captain = is_captain
        self.pre_flight_checks_done = False

    def perform_duty(self) -> str:
        """Выполняет предрейсовый чек-лист и пилотирование."""
        if not self.is_on_shift:
            raise ValueError(f"Пилот {self.full_name} не на смене.")
        self.pre_flight_checks_done = True
        role = "КВС (Капитан)" if self.is_captain else "Второй пилот"
        return f"{role} {self.full_name} выполнил чек-лист и готов к вылету."

    def conduct_preflight_briefing(self, plan: FlightPlan | None = None) -> str:
        """Проводит предполетный брифинг для экипажа самолета."""
        if not self.is_on_shift:
            raise ValueError(f"Пилот {self.full_name} не на смене.")
        corridor_info = f" по коридору {plan.air_corridor}" if plan else ""
        return f"Пилот {self.full_name} провел предполетный брифинг экипажа{corridor_info}."

    def record_landing(self) -> None:
        """Фиксирует успешное выполнение посадки воздушного судна."""
        self.pre_flight_checks_done = False
