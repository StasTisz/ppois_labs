"""Модуль бортпроводника воздушного судна."""

from __future__ import annotations

from typing import TYPE_CHECKING

from lab3.domain.people.crew_member import CrewMember

if TYPE_CHECKING:
    from lab3.domain.people.passenger import Passenger


class FlightAttendant(CrewMember):
    """Бортпроводник."""

    def __init__(
        self,
        first_name: str,
        last_name: str,
        passport_number: str,
        salary: float,
        languages: list[str] | None = None,
    ) -> None:
        """Инициализирует экземпляр класса FlightAttendant."""
        super().__init__(first_name, last_name, passport_number, salary)
        self.languages = languages or ["Русский"]
        self.safety_briefing_done = False

    def perform_duty(self) -> str:
        """Проводит инструктаж и обеспечивает безопасность салона."""
        if not self.is_on_shift:
            raise ValueError(f"Бортпроводник {self.full_name} не на смене.")
        self.safety_briefing_done = True
        langs = ", ".join(self.languages)
        return f"Бортпроводник {self.full_name} проводит предполетный инструктаж пассажиров (языки: {langs})."

    def demonstrate_safety_equipment(self) -> str:
        """Проводит инструктаж пассажиров по аварийно-спасательному оборудованию."""
        return f"Бортпроводник {self.full_name} продемонстрировал аварийно-спасательное оборудование салона."

    def serve_passengers(self, passengers_count: int) -> str:
        """Организует сервисное бортовое обслуживание пассажиров питанием и напитками."""
        if passengers_count < 0:
            raise ValueError("Число пассажиров не может быть отрицательным.")
        return f"Бортпроводник {self.full_name} обслужил {passengers_count} пассажиров на борту."

    def assist_passenger(self, passenger: Passenger) -> str:
        """Оказывает индивидуальную помощь пассажиру на борту самолета."""
        return f"Бортпроводник {self.full_name} оказал помощь пассажиру {passenger.full_name}."
