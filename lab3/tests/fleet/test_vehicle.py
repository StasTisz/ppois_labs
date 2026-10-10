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

    v.requires_maintenance = True
    v.perform_maintenance()
    assert v.requires_maintenance is False
