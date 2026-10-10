import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.fuel_truck import FuelTruck
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft


def test_fuel_truck():
    truck = FuelTruck("Scania-Fuel", 45.0, "FT-88", tank_capacity=10000.0)
    plane = PassengerAircraft("A320", 820.0, "EW-303PA", 12000.0, 160)

    assert truck.current_fuel == 10000.0
    truck.refuel_aircraft(plane, 4000.0)
    assert plane.current_fuel == 4000.0
    assert truck.current_fuel == 6000.0

    with pytest.raises(CapacityExceededException):
        truck.refuel_aircraft(plane, 8000.0)

    truck.perform_maintenance()
    assert truck.pump_calibrated is True
    assert truck.filter_replaced is True
