from __future__ import annotations

from lab3.domain.people.employee import Employee


class SecurityOfficer(Employee):
    def perform_duty(self) -> str:
        return f"Офицер СБ {self.full_name} осуществляет досмотр в зоне контроля."
