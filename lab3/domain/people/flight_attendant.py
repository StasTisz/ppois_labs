from __future__ import annotations

from lab3.domain.people.crew_member import CrewMember


class FlightAttendant(CrewMember):
    def __init__(
            self, first_name: str, last_name: str, passport_number: str,
            salary: float, languages: list[str]
    ) -> None:
        super().__init__(first_name, last_name, passport_number, salary)
        self.languages = languages
        self.safety_briefing_done = False

    def perform_duty(self) -> str:
        if not self.is_on_shift:
            raise ValueError(f"Бортпроводник {self.full_name} не на смене.")
        self.safety_briefing_done = True
        return f"Бортпроводник {self.full_name} провел инструктаж по безопасности."
