import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.fleet.cargo_aircraft import CargoAircraft
from lab3.domain.fleet.private_jet import PrivateJet


def test_passenger_aircraft():
    plane = PassengerAircraft("B737", 850.0, "RA-11111", 20000.0, 180)
    assert plane.tail_number == "RA-11111"
    assert plane.current_fuel == 0.0

    plane.refuel(5000.0)
    assert plane.current_fuel == 5000.0

    with pytest.raises(ValueError):
        plane.refuel(-100.0)
    with pytest.raises(CapacityExceededException):
        plane.refuel(30000.0)

    plane.board_passengers(100)
    assert plane.passengers_count == 100
    with pytest.raises(CapacityExceededException):
        plane.board_passengers(100)

    plane.take_off()
    assert plane.is_in_flight is True
    plane.land()
    assert plane.is_in_flight is False
    assert plane.requires_maintenance is True

    plane.perform_maintenance()
    assert plane.requires_maintenance is False
    assert plane.oxygen_masks_tested is True
    assert plane.disembark_passengers() == 100
    assert plane.passengers_count == 0


def test_cargo_aircraft():
    cargo = CargoAircraft("IL-76", 750.0, "RA-22222", 40000.0, 50000.0)
    cargo.load_cargo(20000.0)
    assert cargo.current_payload_kg == 20000.0

    with pytest.raises(CapacityExceededException):
        cargo.load_cargo(40000.0)

    assert cargo.unload_cargo() == 20000.0
    assert cargo.current_payload_kg == 0.0

    cargo.perform_maintenance()
    assert cargo.winch_mechanism_inspected is True


def test_private_jet():
    jet = PrivateJet("Gulfstream", 900.0, "RA-33333", 15000.0, "Mr. Smith")
    assert jet.owner_name == "Mr. Smith"
    jet.order_vip_catering()
    assert jet.is_vip_catered is True
    jet.perform_maintenance()
    assert jet.satellite_comms_calibrated is True
