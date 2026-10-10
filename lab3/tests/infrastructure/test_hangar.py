import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.fleet.passenger_aircraft import PassengerAircraft
from lab3.domain.infrastructure.hangar import Hangar


def test_hangar():
    hangar = Hangar("H-1", capacity=1)
    plane1 = PassengerAircraft("P1", 800.0, "RA-H1", 1000.0, 100)
    plane2 = PassengerAircraft("P2", 800.0, "RA-H2", 1000.0, 100)

    hangar.store_aircraft(plane1)
    with pytest.raises(CapacityExceededException):
        hangar.store_aircraft(plane2)

    hangar.release_aircraft(plane1)
    hangar.release_aircraft(plane2)
