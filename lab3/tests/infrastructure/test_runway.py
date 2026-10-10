import pytest
from lab3.domain.exceptions import RunwayBusyException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.runway import Runway


def test_runway():
    runway = Runway("12L", 3200)
    plane1 = PassengerAircraft("P1", 800.0, "RA-1", 1000.0, 100)
    plane2 = PassengerAircraft("P2", 800.0, "RA-2", 1000.0, 100)

    assert runway.is_busy is False
    runway.occupy(plane1)
    assert runway.is_busy is True
    assert runway.current_aircraft == plane1

    with pytest.raises(RunwayBusyException):
        runway.occupy(plane2)

    runway.clear()
    assert runway.is_busy is False
    assert runway.current_aircraft is None
