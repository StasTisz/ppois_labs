from __future__ import annotations

from lab3.domain.people.crew_member import CrewMember


class Pilot(CrewMember):
    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, license_type: str, is_captain: bool = False
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.license_type = license_type
        self.is_captain = is_captain
        self.pre_flight_checks_done = False

    def perform_duty(self) -> str:
        if not self.is_on_shift:
            raise ValueError(f"Пилот {self.full_name} не на смене.")
        self.pre_flight_checks_done = True
        role = "КВС (Капитан)" if self.is_captain else "Второй пилот"
        return f"{role} {self.full_name} выполнил чек-лист и готов к вылету."
