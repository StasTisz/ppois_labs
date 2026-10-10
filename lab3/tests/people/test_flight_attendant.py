import pytest
from lab3.domain.people.flight_attendant import FlightAttendant


def test_flight_attendant():
    fa = FlightAttendant("Елена", "Е", "P-111", 1500.0, ["RU", "EN"])
    with pytest.raises(ValueError):
        fa.perform_duty()

    fa.clock_in()
    msg = fa.perform_duty()
    assert "инструктаж" in msg
    assert fa.safety_briefing_done is True
