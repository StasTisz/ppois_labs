import pytest
from lab3.domain.fleet.ground_vehicle import GroundVehicle


class DummyGroundVehicle(GroundVehicle):
    def perform_maintenance(self) -> None:
        self.requires_maintenance = False


def test_ground_vehicle():
    gv = DummyGroundVehicle("Loader", 35.0, "GV-1234")
    assert gv.license_plate == "GV-1234"
    assert gv.is_available is True

    gv.dispatch()
    assert gv.is_available is False

    with pytest.raises(ValueError):
        gv.dispatch()

    gv.release()
    assert gv.is_available is True
