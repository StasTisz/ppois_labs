import pytest
from lab3.domain.exceptions import BaggageOverweightException
from lab3.domain.operations.baggage import Baggage
from lab3.domain.people.passenger import Passenger


def test_baggage():
    p = Passenger("П", "П", "P-1")
    bag_ok = Baggage(20.0, p)
    assert bag_ok.owner == p
    assert bag_ok.owner_id == p.person_id
    bag_ok.check_weight()

    bag_heavy = Baggage(25.0, p)
    with pytest.raises(BaggageOverweightException):
        bag_heavy.check_weight()

    bag_str = Baggage(10.0, "str-id")
    assert bag_str.owner is None
    assert bag_str.owner_id == "str-id"
