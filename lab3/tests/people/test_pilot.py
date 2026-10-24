import pytest

from lab3.domain.people.pilot import Pilot


def test_pilot():
    cap = Pilot("Дмитрий", "Д", "P-789", 4000.0, "ATPL", is_captain=True)
    with pytest.raises(ValueError):
        cap.perform_duty()

    with pytest.raises(ValueError):
        cap.conduct_preflight_briefing()

    cap.clock_in()
    msg = cap.perform_duty()
    assert "КВС (Капитан)" in msg
    assert cap.pre_flight_checks_done is True

    brief = cap.conduct_preflight_briefing()
    assert "предполетный брифинг" in brief

    cap.record_landing()
    assert cap.pre_flight_checks_done is False

    fo = Pilot("Олег", "О", "P-790", 2500.0, "CPL", is_captain=False)
    fo.clock_in()
    assert "Второй пилот" in fo.perform_duty()
