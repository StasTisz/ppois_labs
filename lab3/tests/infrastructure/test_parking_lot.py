import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.infrastructure.parking_lot import ParkingLot


def test_parking_lot():
    lot = ParkingLot("P-Short", capacity=2)
    lot.park_car("0001-AA")
    lot.park_car("0002-AA")

    with pytest.raises(CapacityExceededException):
        lot.park_car("0003-AA")

    lot.remove_car("0001-AA")
    lot.remove_car("9999-XX")
