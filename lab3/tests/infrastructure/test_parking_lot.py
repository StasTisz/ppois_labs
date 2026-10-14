import pytest

from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.ground_vehicle import GroundVehicle
from lab3.domain.infrastructure.parking_lot import ParkingLot


def test_parking_lot():
    lot = ParkingLot("P-Short", capacity=2)
    v1 = GroundVehicle("ServiceVan", 60.0, "0001-AA")
    v2 = GroundVehicle("ServiceVan", 60.0, "0002-AA")
    v3 = GroundVehicle("ServiceVan", 60.0, "0003-AA")

    lot.park_car(v1)
    lot.park_car(v2)
    assert lot.parked_vehicles_count == 2

    with pytest.raises(CapacityExceededException):
        lot.park_car(v3)

    lot.remove_car(v1)
    assert lot.parked_vehicles_count == 1
    other_v = GroundVehicle("Car", 50.0, "9999-XX")
    lot.remove_car(other_v)
