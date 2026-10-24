import pytest

from lab3.domain.fleet.vehicle import Vehicle


class DummyVehicle(Vehicle):
    def perform_maintenance(self) -> None:
        self.requires_maintenance = False


def test_vehicle():
    v = DummyVehicle("Model-X", 120.0)
    assert v.model == "Model-X"
    assert v.max_speed == 120.0
    assert v.requires_maintenance is False
    assert v.operating_hours == 0.0

    v.log_hours(100.0)
    assert v.operating_hours == 100.0
    assert v.requires_maintenance is False

    with pytest.raises(ValueError):
        v.log_hours(-10.0)

    v.log_hours(450.0)
    assert v.operating_hours == 550.0
    assert v.requires_maintenance is True

    v.perform_maintenance()
    assert v.requires_maintenance is False

    v.mark_for_service()
    assert v.requires_maintenance is True
