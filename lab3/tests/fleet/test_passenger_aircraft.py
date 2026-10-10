import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft


def test_passenger_aircraft():
    plane = PassengerAircraft("B737", 850.0, "EW-101PA", 20000.0, max_passengers=180)
    assert plane.max_passengers == 180
    assert plane.passengers_count == 0

    plane.board_passengers(150)
    assert plane.passengers_count == 150

    with pytest.raises(CapacityExceededException):
        plane.board_passengers(40)

    disembarked = plane.disembark_passengers()
    assert disembarked == 150
    assert plane.passengers_count == 0

    plane.perform_maintenance()
    assert plane.oxygen_masks_tested is True
    assert plane.cabin_pressurization_ok is True
    assert plane.requires_maintenance is False
