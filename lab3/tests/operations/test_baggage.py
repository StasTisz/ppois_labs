import pytest

from lab3.domain.exceptions import BaggageOverweightException
from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger


def test_baggage():
    p = Passenger("П", "П", "P-1")
    bag_ok = Baggage(20.0, p)
    assert bag_ok.owner == p
    bag_ok.check_weight()

    bag_heavy = Baggage(25.0, p)
    with pytest.raises(BaggageOverweightException):
        bag_heavy.check_weight()

    p2 = Passenger("А", "Б", "P-2")
    bag_p2 = Baggage(10.0, p2)
    assert bag_p2.owner == p2
    assert bag_p2.weight_kg == 10.0
