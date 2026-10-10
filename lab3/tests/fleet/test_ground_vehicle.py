import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.baggage_tractor import BaggageTractor
from lab3.domain.fleet.fuel_truck import FuelTruck
from lab3.domain.fleet.follow_me_car import FollowMeCar
from lab3.domain.fleet.passenger_bus import PassengerBus
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft


def test_ground_vehicles():
    tractor = BaggageTractor("T-1", 30.0, "A001AA", max_carts=2)
    tractor.attach_cart()
    assert tractor.current_carts == 1
    tractor.attach_cart()
    with pytest.raises(CapacityExceededException):
        tractor.attach_cart()
    tractor.detach_all_carts()
    assert tractor.current_carts == 0
    tractor.perform_maintenance()
    assert tractor.tow_hitch_greased is True

    plane = PassengerAircraft("A320", 800.0, "RA-1", 10000.0, 150)
    truck = FuelTruck("FT-1", 40.0, "B002BB", 5000.0)
    truck.refuel_aircraft(plane, 3000.0)
    assert plane.current_fuel == 3000.0
    assert truck.current_fuel == 2000.0
    with pytest.raises(CapacityExceededException):
        truck.refuel_aircraft(plane, 3000.0)
    truck.perform_maintenance()
    assert truck.filter_replaced is True

    car = FollowMeCar("FMC-1", 60.0, "C003CC")
    msg = car.lead_aircraft(plane, "Gate A1")
    assert "RA-1" in msg
    car.perform_maintenance()
    assert car.lightbar_tested is True

    bus = PassengerBus("Bus-1", 40.0, "D004DD", capacity=50)
    bus.board(30)
    assert bus.passengers_count == 30
    with pytest.raises(CapacityExceededException):
        bus.board(30)
    assert bus.drop_off() == 30
    assert bus.passengers_count == 0
    bus.perform_maintenance()
    assert bus.doors_pneumatics_checked is True
