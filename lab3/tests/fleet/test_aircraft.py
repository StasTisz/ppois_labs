import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.aircraft import Aircraft


class DummyAircraft(Aircraft):
    def perform_maintenance(self) -> None:
        self.requires_maintenance = False


def test_aircraft_base():
    craft = DummyAircraft("TestCraft", 900.0, "TA-001", 10000.0)
    assert craft.tail_number == "TA-001"
    assert craft.current_fuel == 0.0
    assert craft.is_in_flight is False

    craft.refuel(4000.0)
    assert craft.current_fuel == 4000.0

    with pytest.raises(ValueError):
        craft.refuel(-500.0)

    with pytest.raises(CapacityExceededException):
        craft.refuel(7000.0)

    craft.take_off()
    assert craft.is_in_flight is True

    craft.land()
    assert craft.is_in_flight is False
    assert craft.requires_maintenance is True
