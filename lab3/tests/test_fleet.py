import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet import PassengerAircraft, CargoAircraft, PrivateJet, BaggageTractor, FuelTruck, FollowMeCar, \
    PassengerBus


def test_passenger_aircraft_fuel_and_passengers():
    plane = PassengerAircraft("B737", 850.0, "RA-123", 20000.0, 150)
    plane.refuel(10000.0)
    assert plane.current_fuel == 10000.0

    with pytest.raises(CapacityExceededException):
        plane.refuel(15000.0)

    with pytest.raises(ValueError):
        plane.refuel(-500.0)

    plane.board_passengers(100)
    with pytest.raises(CapacityExceededException):
        plane.board_passengers(60)

    disembarked = plane.disembark_passengers()
    assert disembarked == 100
    assert plane.passengers_count == 0


def test_passenger_aircraft_flight_cycle():
    plane = PassengerAircraft("A320", 850.0, "VP-BCA", 15000.0, 180)
    assert not plane.is_in_flight
    plane.take_off()
    assert plane.is_in_flight
    plane.land()
    assert not plane.is_in_flight
    assert plane.requires_maintenance

    plane.perform_maintenance()
    assert not plane.requires_maintenance
    assert plane.oxygen_masks_tested
    assert plane.cabin_pressurization_ok


def test_cargo_aircraft_load():
    cargo = CargoAircraft("IL-76", 750.0, "RA-765", 40000.0, 50000.0)
    cargo.load_cargo(30000.0)
    with pytest.raises(CapacityExceededException):
        cargo.load_cargo(25000.0)

    unloaded = cargo.unload_cargo()
    assert unloaded == 30000.0
    assert cargo.current_payload_kg == 0.0

    cargo.perform_maintenance()
    assert cargo.cargo_hydraulics_ok


def test_private_jet_vip():
    jet = PrivateJet("Gulfstream", 900.0, "VIP-1", 10000.0, "Corp")
    assert not jet.is_vip_catered
    jet.order_vip_catering()
    assert jet.is_vip_catered

    jet.perform_maintenance()
    assert jet.satellite_comms_calibrated


def test_baggage_tractor():
    tractor = BaggageTractor("Tug", 30.0, "TX-1", 2)
    tractor.attach_cart()
    tractor.attach_cart()
    with pytest.raises(CapacityExceededException):
        tractor.attach_cart()

    tractor.detach_all_carts()
    assert tractor.current_carts == 0
    tractor.perform_maintenance()
    assert tractor.tow_hitch_greased


def test_fuel_truck_refueling():
    truck = FuelTruck("Volvo", 60.0, "FT-99", 20000.0)
    plane = PassengerAircraft("B737", 850.0, "RA-111", 15000.0, 150)

    truck.refuel_aircraft(plane, 10000.0)
    assert truck.current_fuel == 10000.0
    assert plane.current_fuel == 10000.0

    with pytest.raises(CapacityExceededException):
        truck.refuel_aircraft(plane, 15000.0)

    truck.perform_maintenance()
    assert truck.pump_calibrated


def test_follow_me_car():
    car = FollowMeCar("Skoda", 120.0, "FM-01")
    plane = PassengerAircraft("B737", 850.0, "RA-111", 15000.0, 150)
    result = car.lead_aircraft(plane, "Gate 5")
    assert "успешно сопровожден" in result
    car.perform_maintenance()
    assert car.lightbar_tested


def test_passenger_bus():
    bus = PassengerBus("Cobus", 40.0, "PB-12", 80)
    bus.board(50)
    with pytest.raises(CapacityExceededException):
        bus.board(40)
    assert bus.drop_off() == 50
    bus.perform_maintenance()
    assert bus.doors_pneumatics_checked


def test_ground_vehicle_dispatch():
    bus = PassengerBus("Cobus", 40.0, "PB-12", 80)
    bus.dispatch()
    with pytest.raises(ValueError):
        bus.dispatch()
    bus.release()
    assert bus.is_available