import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.passenger_bus import PassengerBus


def test_passenger_bus():
    bus = PassengerBus("Cobus-3000", 40.0, "PB-12", capacity=60)
    assert bus.passengers_count == 0

    bus.board(40)
    assert bus.passengers_count == 40

    with pytest.raises(CapacityExceededException):
        bus.board(30)

    dropped = bus.drop_off()
    assert dropped == 40
    assert bus.passengers_count == 0

    bus.perform_maintenance()
    assert bus.doors_pneumatics_checked is True
