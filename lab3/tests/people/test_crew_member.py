import pytest
from lab3.domain.people.crew_member import CrewMember


class DummyCrew(CrewMember):
    def perform_duty(self) -> str:
        return "В полёте"


def test_crew_member():
    crew = DummyCrew("Алексей", "А", "P-456", 2500.0, max_monthly_hours=80)
    assert crew.flight_hours == 0

    crew.log_flight_hours(40)
    assert crew.flight_hours == 40

    with pytest.raises(ValueError):
        crew.log_flight_hours(50)
