import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.cargo_aircraft import CargoAircraft


def test_cargo_aircraft():
    cargo = CargoAircraft("IL-76", 750.0, "EW-202TR", 35000.0, max_payload_kg=40000.0)
    assert cargo.current_payload_kg == 0.0

    cargo.load_cargo(25000.0)
    assert cargo.current_payload_kg == 25000.0

    with pytest.raises(CapacityExceededException):
        cargo.load_cargo(20000.0)

    unloaded = cargo.unload_cargo()
    assert unloaded == 25000.0
    assert cargo.current_payload_kg == 0.0

    cargo.perform_maintenance()
    assert cargo.cargo_hydraulics_ok is True
    assert cargo.winch_mechanism_inspected is True
