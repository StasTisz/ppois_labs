from __future__ import annotations

from lab3.domain.people.crew_member import CrewMember


class FlightAttendant(CrewMember):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        languages: list[str] | None = None,
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.languages = languages or ["Русский"]
        self.safety_briefing_done = False

    def perform_duty(self) -> str:
        if not self.is_on_shift:
            raise ValueError(f"Бортпроводник {self.full_name} не на смене.")
        self.safety_briefing_done = True
        langs = ", ".join(self.languages)
        return f"Бортпроводник {self.full_name} проводит предполетный инструктаж пассажиров (языки: {langs})."

    def demonstrate_safety_equipment(self) -> str:
        return f"Бортпроводник {self.full_name} продемонстрировал аварийно-спасательное оборудование салона."

    def serve_passengers(self, passengers_count: int) -> str:
        if passengers_count < 0:
            raise ValueError("Число пассажиров не может быть отрицательным.")
        return f"Бортпроводник {self.full_name} обслужил {passengers_count} пассажиров на борту."
