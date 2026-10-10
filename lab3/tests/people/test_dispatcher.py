from lab3.domain.people.dispatcher import Dispatcher


def test_dispatcher():
    disp = Dispatcher("Максим", "М", "P-222", 2200.0, clearance_level=3)
    assert disp.clearance_level == 3
    msg = disp.perform_duty()
    assert "3 каналах" in msg
    assert disp.active_channels == 3
