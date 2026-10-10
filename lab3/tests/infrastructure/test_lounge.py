import pytest
from lab3.domain.exceptions import CapacityExceededException
from lab3.domain.infrastructure.lounge import Lounge
from lab3.domain.people.passenger import Passenger


def test_lounge():
    lounge = Lounge("Business Class Lounge", capacity=2, is_vip=True)
    p1 = Passenger("А", "А", "P-1")
    p2 = Passenger("Б", "Б", "P-2")
    p3 = Passenger("В", "В", "P-3")

    lounge.enter(p1)
    lounge.enter(p2)
    assert lounge.current_occupancy == 2

    with pytest.raises(CapacityExceededException):
        lounge.enter(p3)

    lounge.exit(p1)
    assert lounge.current_occupancy == 1
    lounge.exit(p3)
    assert lounge.current_occupancy == 1
