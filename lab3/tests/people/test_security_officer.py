import pytest

from lab3.domain.people.passenger import Passenger
from lab3.domain.people.security_officer import SecurityOfficer


def test_security_officer():
    so = SecurityOfficer("Виктор", "В", "P-333", 1400.0)
    assert "досмотр" in so.perform_duty()
    assert "SEC-P-33" in so.badge_number or "SEC" in so.badge_number
    assert len(so.detained_passengers) == 0

    p = Passenger("Подозрительный", "П", "P-SUS")
    so.detain_passenger(p, "Попытка проноса запрещенных предметов")
    assert len(so.detained_passengers) == 1

    # Copy protection
    dt = so.detained_passengers
    dt.clear()
    assert len(so.detained_passengers) == 1

    with pytest.raises(ValueError):
        so.detain_passenger(p, "   ")

    so.release_passenger(p)
    assert len(so.detained_passengers) == 0
